---
title: How do I invite Cloud users?
---

{% include /cloud-config/cloud-summary-users.md %}

## Before you begin

{% include /cloud-config/cloud-user-admin-role-needed.md %}
{% include /cloud/cloud-before-begin.md %}
* [Learn how to manage cloud users](/cloud/cloud-configuration/cloud-users-manage)

{% include /cloud-config/cloud-username-nochange.md %}

## How do I invite a user to my organization?

When you invite a user, FeatureBase will:
* generate a unique invitation URL that expires after 7 days
* send the invitation URL to the provided email address
* add the user email address to the **Invited users** list

### Invite a user

* Click **Configuration** > **Manage users**.
* Click **Invite new user**.
* Enter one or more email addresses, using commas to separate them.
* Click **Send invitation**.

## Provide invitation URL (optional)

You can copy the invitation URL and provide it to the user if required.

* Click **Configuration** > **Manage users**.
* Scroll to **Invited users**.
* {%  include /cloud-icons/icon-edit-unicode.md %} on the user > **Copy invite URL**.

## Next step

* [Learn how to change user roles](/cloud/cloud-configuration/cloud-user-edit-role)
