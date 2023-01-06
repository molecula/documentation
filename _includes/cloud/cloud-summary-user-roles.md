FeatureBase Cloud supports two user roles for **active** accounts:
* User - granted automatically to all verified accounts on first login
* Administrator - granted by existing account with administrator role

Each role contains a collection of system privileges.

## User management privileges

| Privilege | User role | Administrator role |
|---|---|---|
| [Login](/cloud/fbc-part2-login) | Yes | Yes |
| [Invite users](/cloud/cloud-configuration/cloud-user-invite) | No | Yes |
| Copy invite URL | No | Yes |
| [Read user profiles](/cloud/cloud-configuration/cloud-users-view-search) | Own account | Yes |
| Update user profile | [Own account](/cloud/my-account/cloud-user-personal-update) | Yes |
| [Alter role](/cloud/cloud-configuration/cloud-user-edit-role) | No | All but own account |
| [Activate user account](/cloud/cloud-configuration/cloud-user-deactivate) | No | Yes |
| [Deactivate user account](/cloud/cloud-configuration/cloud-user-deactivate) | No | Yes |

## Database management privileges

| Privilege | User role | Administrator role |
|---|---|---|
| [Create databases](/cloud/cloud-databases/cloud-db-create) | Yes | Yes |
| Read & query databases | Yes | Yes |
| Delete databases | Own database | All |

## Table management privileges

| Privilege | User role | Administrator role |
|---|---|---|
| [Create tables](/cloud/cloud-tables/cloud-table-create) | Yes | Yes |
| Read & query tables | Yes | Yes |
| [Add table column](/cloud/cloud-tables/cloud-table-add-column) | Own tables | All |
| [Delete table column](/cloud/cloud-tables/cloud-table-delete-column) | Own tables | All |
| [Delete tables](/cloud/cloud-tables/cloud-table-drop) | Own tables | All |

## Data source management privileges

| Privilege | User role | Administrator role |
|---|---|---|
| Create data sources | Yes | Yes |
| Read & query data sources | Yes | Yes |
| Update data sources | Own data sources | All |
| Delete data sources | Own data sources | All |

## Organization management privileges

| Privilege | User role | Administrator role |
|---|---|---|
| Read organization details | No | Yes |
| [Update organization details](/cloud/cloud-configuration/cloud-org-address) | No | Yes |
| [Update billing contact](/cloud/cloud-configuration/cloud-org-update-billing) | No | Yes |
| [Update technical contact](/cloud/cloud-configuration/cloud-org-update-tech-contact) | No | Yes |
