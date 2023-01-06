FeatureBase Cloud supports two user roles for **active** accounts:
* User - granted automatically to all verified accounts on first login
* Administrator - granted by existing account with administrator role

Each role contains a collection of system privileges.

## User management privileges

| Privilege | User role | Administrator role |
|---|---|---|
| Login | Yes | Yes |
| Invite users | No | Yes |
| Copy invite URL | No | Yes |
| Read user profiles | Own account | Yes |
| Update user profile | Own account | Yes |
| Alter role | No | All but own account |
| Activate user account | No | Yes |
| Deactivate user account | No | Yes |

## Database management privileges

| Privilege | User role | Administrator role |
|---|---|---|
| Create databases | Yes | Yes |
| Read & query databases | Yes | Yes |
| Update databases | Own database | All |
| Delete databases | Own database | All |

## Table management privileges

| Privilege | User role | Administrator role |
|---|---|---|
| Create tables | Yes | Yes |
| Read & query tables | Yes | Yes |
| Update tables | Own tables | All |
| Delete tables | Own tables | All |

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
| Update organization details | No | Yes |
| Update billing contact | No | Yes |
| Update technical contact | No | Yes |
