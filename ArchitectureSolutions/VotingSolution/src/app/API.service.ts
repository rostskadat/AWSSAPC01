/* tslint:disable */
/* eslint-disable */
//  This file was automatically generated and should not be edited.
import { Injectable } from "@angular/core";
import API, { graphqlOperation, GraphQLResult } from "@aws-amplify/api-graphql";
import { Observable } from "zen-observable-ts";

export interface SubscriptionResponse<T> {
  value: GraphQLResult<T>;
}

export type CreateVoteInput = {
  id?: string | null;
  election: string;
  vote: string;
};

export type ModelVoteConditionInput = {
  election?: ModelStringInput | null;
  vote?: ModelStringInput | null;
  and?: Array<ModelVoteConditionInput | null> | null;
  or?: Array<ModelVoteConditionInput | null> | null;
  not?: ModelVoteConditionInput | null;
};

export type ModelStringInput = {
  ne?: string | null;
  eq?: string | null;
  le?: string | null;
  lt?: string | null;
  ge?: string | null;
  gt?: string | null;
  contains?: string | null;
  notContains?: string | null;
  between?: Array<string | null> | null;
  beginsWith?: string | null;
  attributeExists?: boolean | null;
  attributeType?: ModelAttributeTypes | null;
  size?: ModelSizeInput | null;
};

export enum ModelAttributeTypes {
  binary = "binary",
  binarySet = "binarySet",
  bool = "bool",
  list = "list",
  map = "map",
  number = "number",
  numberSet = "numberSet",
  string = "string",
  stringSet = "stringSet",
  _null = "_null"
}

export type ModelSizeInput = {
  ne?: number | null;
  eq?: number | null;
  le?: number | null;
  lt?: number | null;
  ge?: number | null;
  gt?: number | null;
  between?: Array<number | null> | null;
};

export type Vote = {
  __typename: "Vote";
  id?: string;
  election?: string;
  vote?: string;
  createdAt?: string;
  updatedAt?: string;
};

export type UpdateVoteInput = {
  id: string;
  election?: string | null;
  vote?: string | null;
};

export type DeleteVoteInput = {
  id?: string | null;
};

export type ModelVoteFilterInput = {
  id?: ModelIDInput | null;
  election?: ModelStringInput | null;
  vote?: ModelStringInput | null;
  and?: Array<ModelVoteFilterInput | null> | null;
  or?: Array<ModelVoteFilterInput | null> | null;
  not?: ModelVoteFilterInput | null;
};

export type ModelIDInput = {
  ne?: string | null;
  eq?: string | null;
  le?: string | null;
  lt?: string | null;
  ge?: string | null;
  gt?: string | null;
  contains?: string | null;
  notContains?: string | null;
  between?: Array<string | null> | null;
  beginsWith?: string | null;
  attributeExists?: boolean | null;
  attributeType?: ModelAttributeTypes | null;
  size?: ModelSizeInput | null;
};

export type ModelVoteConnection = {
  __typename: "ModelVoteConnection";
  items?: Array<Vote | null> | null;
  nextToken?: string | null;
};

export type CreateVoteMutation = {
  __typename: "Vote";
  id: string;
  election: string;
  vote: string;
  createdAt: string;
  updatedAt: string;
};

export type UpdateVoteMutation = {
  __typename: "Vote";
  id: string;
  election: string;
  vote: string;
  createdAt: string;
  updatedAt: string;
};

export type DeleteVoteMutation = {
  __typename: "Vote";
  id: string;
  election: string;
  vote: string;
  createdAt: string;
  updatedAt: string;
};

export type GetVoteQuery = {
  __typename: "Vote";
  id: string;
  election: string;
  vote: string;
  createdAt: string;
  updatedAt: string;
};

export type ListVotesQuery = {
  __typename: "ModelVoteConnection";
  items?: Array<{
    __typename: "Vote";
    id: string;
    election: string;
    vote: string;
    createdAt: string;
    updatedAt: string;
  } | null> | null;
  nextToken?: string | null;
};

export type OnCreateVoteSubscription = {
  __typename: "Vote";
  id: string;
  election: string;
  vote: string;
  createdAt: string;
  updatedAt: string;
};

export type OnUpdateVoteSubscription = {
  __typename: "Vote";
  id: string;
  election: string;
  vote: string;
  createdAt: string;
  updatedAt: string;
};

export type OnDeleteVoteSubscription = {
  __typename: "Vote";
  id: string;
  election: string;
  vote: string;
  createdAt: string;
  updatedAt: string;
};

@Injectable({
  providedIn: "root"
})
export class APIService {
  async CreateVote(
    input: CreateVoteInput,
    condition?: ModelVoteConditionInput
  ): Promise<CreateVoteMutation> {
    const statement = `mutation CreateVote($input: CreateVoteInput!, $condition: ModelVoteConditionInput) {
        createVote(input: $input, condition: $condition) {
          __typename
          id
          election
          vote
          createdAt
          updatedAt
        }
      }`;
    const gqlAPIServiceArguments: any = {
      input
    };
    if (condition) {
      gqlAPIServiceArguments.condition = condition;
    }
    const response = (await API.graphql(
      graphqlOperation(statement, gqlAPIServiceArguments)
    )) as any;
    return <CreateVoteMutation>response.data.createVote;
  }
  async UpdateVote(
    input: UpdateVoteInput,
    condition?: ModelVoteConditionInput
  ): Promise<UpdateVoteMutation> {
    const statement = `mutation UpdateVote($input: UpdateVoteInput!, $condition: ModelVoteConditionInput) {
        updateVote(input: $input, condition: $condition) {
          __typename
          id
          election
          vote
          createdAt
          updatedAt
        }
      }`;
    const gqlAPIServiceArguments: any = {
      input
    };
    if (condition) {
      gqlAPIServiceArguments.condition = condition;
    }
    const response = (await API.graphql(
      graphqlOperation(statement, gqlAPIServiceArguments)
    )) as any;
    return <UpdateVoteMutation>response.data.updateVote;
  }
  async DeleteVote(
    input: DeleteVoteInput,
    condition?: ModelVoteConditionInput
  ): Promise<DeleteVoteMutation> {
    const statement = `mutation DeleteVote($input: DeleteVoteInput!, $condition: ModelVoteConditionInput) {
        deleteVote(input: $input, condition: $condition) {
          __typename
          id
          election
          vote
          createdAt
          updatedAt
        }
      }`;
    const gqlAPIServiceArguments: any = {
      input
    };
    if (condition) {
      gqlAPIServiceArguments.condition = condition;
    }
    const response = (await API.graphql(
      graphqlOperation(statement, gqlAPIServiceArguments)
    )) as any;
    return <DeleteVoteMutation>response.data.deleteVote;
  }
  async GetVote(id: string): Promise<GetVoteQuery> {
    const statement = `query GetVote($id: ID!) {
        getVote(id: $id) {
          __typename
          id
          election
          vote
          createdAt
          updatedAt
        }
      }`;
    const gqlAPIServiceArguments: any = {
      id
    };
    const response = (await API.graphql(
      graphqlOperation(statement, gqlAPIServiceArguments)
    )) as any;
    return <GetVoteQuery>response.data.getVote;
  }
  async ListVotes(
    filter?: ModelVoteFilterInput,
    limit?: number,
    nextToken?: string
  ): Promise<ListVotesQuery> {
    const statement = `query ListVotes($filter: ModelVoteFilterInput, $limit: Int, $nextToken: String) {
        listVotes(filter: $filter, limit: $limit, nextToken: $nextToken) {
          __typename
          items {
            __typename
            id
            election
            vote
            createdAt
            updatedAt
          }
          nextToken
        }
      }`;
    const gqlAPIServiceArguments: any = {};
    if (filter) {
      gqlAPIServiceArguments.filter = filter;
    }
    if (limit) {
      gqlAPIServiceArguments.limit = limit;
    }
    if (nextToken) {
      gqlAPIServiceArguments.nextToken = nextToken;
    }
    const response = (await API.graphql(
      graphqlOperation(statement, gqlAPIServiceArguments)
    )) as any;
    return <ListVotesQuery>response.data.listVotes;
  }
  OnCreateVoteListener: Observable<
    SubscriptionResponse<OnCreateVoteSubscription>
  > = API.graphql(
    graphqlOperation(
      `subscription OnCreateVote {
        onCreateVote {
          __typename
          id
          election
          vote
          createdAt
          updatedAt
        }
      }`
    )
  ) as Observable<SubscriptionResponse<OnCreateVoteSubscription>>;

  OnUpdateVoteListener: Observable<
    SubscriptionResponse<OnUpdateVoteSubscription>
  > = API.graphql(
    graphqlOperation(
      `subscription OnUpdateVote {
        onUpdateVote {
          __typename
          id
          election
          vote
          createdAt
          updatedAt
        }
      }`
    )
  ) as Observable<SubscriptionResponse<OnUpdateVoteSubscription>>;

  OnDeleteVoteListener: Observable<
    SubscriptionResponse<OnDeleteVoteSubscription>
  > = API.graphql(
    graphqlOperation(
      `subscription OnDeleteVote {
        onDeleteVote {
          __typename
          id
          election
          vote
          createdAt
          updatedAt
        }
      }`
    )
  ) as Observable<SubscriptionResponse<OnDeleteVoteSubscription>>;
}
