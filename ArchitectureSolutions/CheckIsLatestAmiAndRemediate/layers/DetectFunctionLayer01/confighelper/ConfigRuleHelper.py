import boto3
import json
import logging

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger('ConfigRuleHelper')
logger.setLevel(logging.INFO)

#
# REFERENCE: https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules_nodejs-sample.html
#

class ConfigRuleHelper(object):
    """This decorator can be used to ease the burden of implementing Compliance Rules

    You can use it as:

    helper = ConfigRuleHelper()

    @helper.compliance_rule
    def is_valid_ami(rule_parameters, configuration_item):
        valid_image_id = 'ami-012345679'
        if (configuration_item["resourceType"] != 'AWS::EC2::Instance'):
            return "NOT_APPLICABLE"
        elif (valid_image_id == configuration_item["configuration"]["imageId"]):
            return "COMPLIANT"
        return "NON_COMPLIANT"

    def lambda_handler(event, context):
        helper(event, context)

    That will make sure that the call is retried if it fails with either
    ConcurrentModificationException or TooManyRequestsException...
    """

    def __init__(self):
        self._config_rule_func = None
        self.config = boto3.client('config')

    def __call__(self, event, context):
        invoking_event = json.loads(event["invokingEvent"])
        rule_parameters = json.loads(event.get("ruleParameters", "{}"))
        configuration_item = self._get_configuration_item(invoking_event)
        if self._is_applicable(event, configuration_item):
            compliance = self._evaluate_compliance(
                rule_parameters, configuration_item)
        else:
            compliance = "NOT_APPLICABLE"
        evaluations = [{
            "ComplianceResourceType": configuration_item["resourceType"],
            "ComplianceResourceId": configuration_item["resourceId"],
            "ComplianceType": compliance,
            "OrderingTimestamp": configuration_item["configurationItemCaptureTime"],
        }]
        result_token= event["resultToken"]
        logger.info(json.dumps(evaluations))
        self.config.put_evaluations(Evaluations=evaluations, ResultToken=result_token)

    def config_rule(self, func):
        """Create a compliance rule.

        Args:
            valid_resource_types ([type]): [description]
            func ([type]): [description]

        Returns:
            [type]: [description]
        """
        self._config_rule_func = func
        return func

    def _is_applicable(self, event, configuration_item):
        """Check whether the resource has been deleted. 

        If the resource was deleted, then the evaluation returns not applicable.

        Returns:
            true: return True if the rule should be appliead, False otherwise
        """
        self._check_defined(event, 'event')
        self._check_defined(configuration_item, 'configurationItem')
        event_left_scope = bool(event["eventLeftScope"])
        status = configuration_item["configurationItemStatus"]
        return (status == 'OK' or status == 'ResourceDiscovered') and not event_left_scope

    def _check_defined(self, reference, referenceName):
        if not reference:
            raise Exception(f"Error: {referenceName} is not defined")
        return reference

    def _evaluate_compliance(self, rule_parameters, configuration_item):
        try:
            return self._config_rule_func(rule_parameters, configuration_item)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return "NON_COMPLIANT"

    def _get_configuration_item(self, invoking_event):
        return invoking_event["configurationItem"]
