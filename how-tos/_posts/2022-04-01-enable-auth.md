---
id: enable-auth
title: How To Enable Authentication and Authorization
sidebar_label: Enable Authentication and Authorization
---
FeatureBase supports authentication and authorization with OAuth2.0 via a configurable identity provider (IdP). Azure Active Directory is supported.

## Authentication
Authentication is the process of confirming a user's identity.

FeatureBase directs unauthenticated users to the "Sign In" page. When the user clicks the sign-in button, they are redirected to the configured IdP's login page. Once the user successfully logs in, the identity provider gives FeatureBase a token to retrieve the user's groups from the configured groups endpoint. Once FeatureBase has retrieved the user's groups, it will return the JWT back to the user in the form of a cookie (called `molecula-chip`). The JWT in this cookie will be used to authorize the user in subsequent requests.

## Authorization
Authorization is the process of validating access to protected resources for a given user.

In the IdP, a user may be assigned to one or more groups. When FeatureBase is configured for auth, a permissions file must be provided. The permissions file maps group IDs to indices and permission levels, and has one group ID for cluster-level admin access. There are two permissions at the index level: read and write.

When a user logs in to FeatureBase, their groups are retrieved from the IdP. These group(s) are then mapped to index-level permissions from the configured permissions file to validate the user's access to a protected resource.

- If no permissions are provided in the permissions file, no access is allowed to FeatureBase.
- Access at the group level can be granted, revoked or changed by updating the permissions file. Changes to the permissions file require a FeatureBase restart.

    **⚠ WARNING:** 
    The `featurebase.conf` and associated `permissions.yml` files _MUST_ be _identical_ across all nodes in a cluster. Failure to do so may result in an insecure cluster.

- Access at the user level can be granted, revoked or changed in the identity provider by changing the user's group memberships. Note that group membership changes may take a moment to propagate to FeatureBase.

## Audit Log
The audit log is a record of requests made to the FeatureBase server. When the FeatureBase server is started, permissions information from the permissions file is logged. Every time a request is made to FeatureBase server, the requested index, user id, user name, query string and IP are logged.

## Configuring Azure Active Directory
The links below reference the API documentation for configuring Azure Active Directory as an identity provider for a third party application.
To configure Azure Active Directory as an IdP:
-  Register FeatureBase as an application using [Create an application registration documentation](https://docs.microsoft.com/en-us/powerapps/developer/data-platform/walkthrough-register-app-azure-active-directory#create-an-application-registration)
    - In step 4, the redirect URL is the fully qualified domain or public IP address for a FeatureBase node with the path `/redirect`, e.g. `https://YOUR-DOMAIN-HERE:10101/redirect`.
    - In step 6, FeatureBase application must have these permissions:
        - Microsoft Graph : Delegated : GroupMember.ReadAll.
        - Microsoft Graph : Delegated : User.Read.All.

- [Create a new application secret key](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret) and add the secret key to the `client-secret` configuration item in `featurebase.conf`.
- [Create groups](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-groups-create-azure-portal#create-a-basic-group-and-add-members) by following steps 1 through 10.
- [Add users to groups](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-groups-create-azure-portal#create-a-basic-group-and-add-members) by following steps 11 through 12.
- Finally, on the App configuration page, on the "Authentication" tab, scroll to
  "Advanced Settings" and toggle "Allow public client flows" to "yes".
!["Image of AzureAD app configuration page with Allow public client flows toggled to yes."](/img/public_client_flows.png)

## Configuring FeatureBase

 **⚠ WARNING:** 
The `featurebase.conf` and associated `permissions.yml` files _MUST_ be _identical_ across all nodes in a cluster. Failure to do so may result in an insecure cluster.


To enable authentication and authorization in FeatureBase, add the following lines to your `featurebase.conf`. More information on these parameters and their values can be found at [this link](/setting-up-featurebase/enterprise/featurebase-configuration)
```
[auth]
 enable = true
 client-id = ""
 client-secret = ""
 authorize-url = ""
 token-url = ""
 group-endpoint-url = ""
 redirect-base-url = ""
 logout-url = ""
 scopes = []
 secret-key = ""
 permissions = ""
 query-log-path = ""
 configured-ips = []
```

Additionally, TLS must be enabled. Refer to [How To Enable TLS](/how-tos/enable-mutual-tls) for more details.

- Create a permissions file: `permissions.yaml`.
    - Copy the example below and update with group ids, index names and permissions.
        - Note that the permission (read or write) must be lower case.
        - Only 1 group is allowed for admin level access. Admin has access to all indexes in FeatureBase.
        ```
        user-groups:
        "<group-id1>":
            "<index1>": "<write>"
            "<index2>": "<read>"
        "<group-id2>":
            "<index1>": "<read>"
        admin: "<groupd-id3>"
        ```

- `client-id` can be obtained from the IdP.
    - In Azure Active Directory, it can be found under the Applications Overview Page.
- `client-secret` can be obtained from the IdP.
- `authorize-url`, `token-url` can be obtained from the IdP.
    - In Azure Active Directory, they can be found under the Applications Overview Page under endpoints tab. If there are two versions available (v1 and v2), use the v2 links.
- `redirect-base-url` uses the same url configured in the IdP without the path `/redirect`. This is usually the URI of your primary featurebase node, e.g. "https://your-ip-here:10101"
- `group-endpoint-url`, `logout-url` and `scopes` can be found in the IdP API documentation.
    - For Azure Active Directory, use this configuration:
    ```
    group-endpoint-url = "https://graph.microsoft.com/v1.0/me/transitiveMemberOf/"
    logout-url = "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
    scopes = ["https://graph.microsoft.com/.default", "offline_access"]
    ```
- `secret-key`: secret key used to secure inter-node communication in a FeatureBase cluster. Run `featurebase keygen` command to generate a key to use.
- `query-log-path`: path for [query audit log](#audit-log).
- `permissions`: path for group permissions file that maps group IDs to index-level access.
- `configured-ips`: list of whitelisted IPs/subnets, admin permissions are granted for any request originating from an IP in this list. Domain names and `0.0.0.0/0` are not allowed options. If list is empty or if option is not set, no IPs are whitelisted. 

### Configure audit logs in FeatureBase
- Create a log file:
    ```
    sudo mkdir -p /var/log/molecula/ && touch /var/log/molecula/query.log
    ```
    If this looks unfamiliar, or this directory has not been set up, refer to [How To Install FeatureBase](/how-tos/install-featurebase).

- Add the path to the `query-log-path` parameter in `featurebase.conf`.

## TLS Configuration
TLS _must_ be enabled when authentication is enabled.  To configure basic TLS, refer to [How To Enable TLS](/how-tos/enable-mutual-tls).

When TLS is enabled, the scheme must be explicitly defined as `https` in `featurebase.conf` and in the command-line.

For example, `bind = "localhost:10101"` must be `bind = "https://localhost:10101"`.

## FAQs
<span id="how-to-get-auth-token"></span>
### How can I get an auth and refresh token?
An auth token is a valid JWT provided by FeatureBase after the user is
authenticated. A refresh token is a token used to refresh an expired auth token.

**⚠ WARNING:** Keep these safe, since they are used to identify and authorize you as a
user. You should _NEVER_ share your auth-token or refresh-token with anyone.

There are two ways to get an auth token in FeatureBase.

1. The first, and easiest method, is to use the `featurebase auth-token` subcommand. Run
`featurebase auth-token` from the command line, and follow the prompts. Once
authentication is complete, your auth-token and refresh-token will be printed to the
screen.

2. The second works if you're already logged in to the lattice UI:
- Right click on the browser, and click on Inspect
!["Inspect"](/img/auth_inspect.png)
- Click on Application
!["Cookie"](/img/auth_inspect_result.png)
- Click on Cookies on the left-side tabs, then click on `molecula-chip`. Copy the Cookie Value, this is the auth token.
- While on the cookies tab, click on `refresh-molecula-chip`. Copy the Cookie Value, this is the refresh token.
!["Molecula-Token"](/img/auth_token.png)


### How can I use an auth token?
To access FeatureBase outside of the UI, an auth token is required. Refer to the [HTTP API](/reference/api/enterprise/http-api#http-api-with-authentication), [gRPC API](/reference/api/enterprise/grpc-api#grpc-api-with-authentication), [backup/restore](/reference/operations/enterprise/backups#backups-with-authentication) or [grafana](/how-tos/use-grafana-plugin#grafana-with-authentication) documentation for details on how to use an auth token to access FeatureBase.
