FeatureBase Cloud supports two user roles for **active** accounts:
* User - granted automatically to all verified accounts on first login
* Administrator - granted by existing account with administrator role

Each role contains a collection of system privileges.

## User management privileges

| Privilege | Applicable role(s) |
|---|---|
| [Login](/cloud/fbc-part2-login) | User, Administrator |
| [Invite users](/cloud/cloud-configuration/cloud-user-invite) | Administrator |
| Copy invite URL | Administrator|
| [Read user profiles](/cloud/cloud-configuration/cloud-users-view-search) | User(Own account), Administrator|
| [Update user profile](/cloud/my-account/cloud-user-personal-update) | User(Own account), Administrator |
| [Alter role](/cloud/cloud-configuration/cloud-user-edit-role) | Administrator(All but own account) |
| [Activate user account](/cloud/cloud-configuration/cloud-user-deactivate) | Administrator |
| [Deactivate user account](/cloud/cloud-configuration/cloud-user-deactivate) | Administrator|

## Database management privileges

| Privilege | Applicable role(s) |
|---|---|
| [Create databases](/cloud/cloud-databases/cloud-db-create) | User, Administrator |
| Read & query databases | User, Administrator |
| Delete databases | User, Administrator |

## Table management privileges

| Privilege | Applicable role(s) |
|---|---|
| [Create tables](/cloud/cloud-tables/cloud-table-create) | User, Administrator |
| Read & query tables | User, Administrator |
| [Add table column](/cloud/cloud-tables/cloud-table-add-column) | User, Administrator|
| [Delete table column](/cloud/cloud-tables/cloud-table-delete-column) | User, Administrator|
| [Delete tables](/cloud/cloud-tables/cloud-table-drop) | User, Administrator |

## Organization management privileges

| Privilege | Applicable role(s) |
|---|---|
| Read organization details | Administrator |
| [Update organization details](/cloud/cloud-configuration/cloud-org-address) | Administrator |
| [Update billing contact](/cloud/cloud-configuration/cloud-org-update-billing) | Administrator |
| [Update technical contact](/cloud/cloud-configuration/cloud-org-update-tech-contact) | Administrator |
