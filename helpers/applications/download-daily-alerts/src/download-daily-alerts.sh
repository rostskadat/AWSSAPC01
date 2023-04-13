#!/bin/bash
#------------------------------------------------------------------------------
#
# FILE: download-daily-alerts.sh
#
# DESCRIPTION:
#   Download the ZTF Alerts for a specific date
#
#------------------------------------------------------------------------------

#==============================================================================
# CONSTANTS DEFINITION SECTION. ONLY "TRUE" CONSTANTS PLEASE
#==============================================================================
ZTF_BASE_URL="https://ztf.uw.edu/alerts/public/ztf_public_%DATE%.tar.gz"

#------------------------------------------------------------------------------
# FUNCTION: usage
#------------------------------------------------------------------------------
usage()
{
    cat >&2 <<EOF

Usage: $(basename $0)

Download the ZTF Alerts for a specific date

General options:
    -h|--help:      This message
    -p|--profile:   Specify the AWS to use. Usefull when working locally 
    -d|--date:      The date of the ZTF Alert tarball to download. In YYYYMMDD Format. Default to today's date.
    -t|--tmp-dir:   The intermediate path where the file should be downloaded (Hint: can be EFS)
    -b|--bucket:    The S3 Bucket used to upload the AVRO files from the ZTF Alert tarball
    -h|--help:      Print this help message.

SYNOPSIS:

Download the current ZTF Alerts tarball in the tmp directory
?> $0 --bucket <Bucket>

Download the ZTF Alerts tarball for the date 20200913 in the S3 bucket
?> $0 --bucket <Bucket> --date 20200913

EOF
}

#==============================================================================
#
# MAIN PROGRAM SECTION.
#
#==============================================================================

#------------------------------------------------------------------------------
# Command line parameter handling
#------------------------------------------------------------------------------
p_profile=
p_date=$(date '+%Y%m%d')
p_tmp_dir=/tmp
p_bucket=
p_no_expand=false
p_debug=false

options=$(getopt --alternative --name $(basename $0) --options "hp:d:t:b:zD" --longoptions help,profile:,date:,tmp-dir:,bucket:,no-expand,debug -- $0 "$@")
if [ $? -ne 0 ]; then
    usage
    exit 1
fi
eval set -- "$options"
while true; do
    case "$1" in
    -p|--profile)   shift; p_profile=$1 ;;
    -d|--date)      shift; p_date=$1 ;;
    -t|--tmp-dir)   shift; p_tmp_dir=$1 ;;
    -b|--bucket)    shift; p_bucket=$1 ;;
       --no-expand) p_no_expand=true ;;
       --debug)     p_debug=true ;;
    -h|--help)      usage; exit 0 ;;
    --) shift; break ;;
    esac
    shift
done

if [ ! -d "${p_tmp_dir}" ]; then
  usage
  echo "Invalid '--tmp-dir' argument: No such directory ${p_tmp_dir}" >&2
  exit 1
fi

ztf_url=$(echo $ZTF_BASE_URL|sed -e "s/%DATE%/${p_date}/")
local_url="${p_tmp_dir}/$(basename ${ztf_url})"

echo "Downloading ${ztf_url} to ${local_url} ..."
curl ${ztf_url} -o ${local_url}

if [ ! -f "${local_url}" ]; then
    echo "Failed to download ${ztf_url}. Bailing out!"  >&2
    exit 1
fi

local_dir=${local_url%.tar.gz}
echo "Expanding ${local_url} into ${local_dir} ..."
mkdir -p ${local_dir}
tar xzf ${local_url} --directory ${local_dir}
rc=$?

if [ ! -z "${p_bucket}" ]; then
    dst_prefix=$(echo -n ${p_date} | sed -E 's#(....)(..)(..)#\1/\2/\3#')
    echo "Syncing ${local_dir} with s3://${p_bucket}/${dst_prefix} ..."
    aws s3 sync ${local_dir} s3://${p_bucket}/${dst_prefix}
    rc=$?
    rm -rf ${local_dir}
else
    rm -f ${local_url}
fi

exit $rc
