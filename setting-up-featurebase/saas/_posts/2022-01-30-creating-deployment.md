---
title: Creating a Deployment
---

---
id: createdeployment
title: Create A Deployment
sidebar_label: Create A Deployment
---

 **⚠ WARNING:** This page contains information that only applies to Molecula's SaaS offering. Additionally, this page represents a work in progress that is subject to frequent changes. 


In the user interface, clicking “Get Started” or “Cloud Manager” from the home page will direct you to the Cloud Manager page where you can create a deployment by clicking “New Deployment”. Today, the tool has [sizes](/setting-up-featurebase/saas/deployments-overview#sizes) based on memory, so all you need to provide is a deployment memory from a drop down and a deployment name. Note the UI will only display the choices your organization has access to, which is determined when you purchase the product. These choices can be queried for programmatically as well and are referred to as “deployment shapes”:


**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.molecula.cloud/v1/service-properties/deployment:shapes' \
--header 'Authorization: Bearer <IdToken>' 
```

The deployment name must be unique within the organization and only contain lower case alphanumeric, hyphen and underscore characters. You can have multiple deployments, so it’s important to name these something meaningful to you and your organization. For example, if you have a customer segmentation deployment and know you’ll have a full staging environment, you might want to name your production deployment as cust_seg_production and your staging deployment as cust_seg_staging. Clicking “Start” will start creating your deployment. This can also be accomplished programmatically:

**HTTP API Reference:**
```shell
curl --location --request POST 'https://api.molecula.cloud/v1/deployments' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' \
--data-raw '--data-raw '{
    "name": "<deployment_name>",
    "deployment_options":{
        "shape": "<deployment_choice>"
    }
}'
```

After clicking “Start”, you will see a new entry populate in the Cloud Manager page with the name you provided. You will also see a status of “CREATING”. This is the state shown as the underlying hardware is provisioned. After a minute or two, the status will update to “RUNNING”, which indicates your deployment is ready to use. The other states you might encounter can be seen [here](/setting-up-featurebase/saas/deployments-overview#states). All of your deployments' statuses can also be queried programmatically.

**HTTP API Reference:**
```shell
curl --location --request GET 'https://api.molecula.cloud/v1/deployments' \
--header 'Authorization: Bearer <IdToken>' \
--header 'Content-Type: application/json' 
```

Once your deployment is in the “RUNNING” state, you are free to start creating tables and loading data.
