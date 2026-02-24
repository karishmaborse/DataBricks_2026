# Upgrade Databricks SDK to the latest version and restart Python to see updated packages
%pip install --upgrade databricks-sdk==0.70.0
%restart_python

from databricks.sdk.service.jobs import JobSettings as Job


CRM_data_Ingestion = Job.from_dict(
    {
        "name": "CRM data Ingestion",
        "description": "This job will create 3 layers: bronze, silver, and gold. It will clean the raw data and then make it ready as a Delta table for various usecases.",
        "tasks": [
            {
                "task_key": "Bronze_layer",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/bronze_layer",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "SIlver_ERP_Customer",
                "depends_on": [
                    {
                        "task_key": "Bronze_layer",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/Silver_layer/ERP/silver_erp_cust_az12.ipynb",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Silver_CRM_layer",
                "depends_on": [
                    {
                        "task_key": "Bronze_layer",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/Silver_layer/CRM/Silver_crm_cust_info",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Gold_Dim_customer",
                "depends_on": [
                    {
                        "task_key": "Silver_CRM_layer",
                    },
                    {
                        "task_key": "SIlver_ERP_Customer",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/Gold_layer/gold_dim_customers",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Silver_ERP_Location",
                "depends_on": [
                    {
                        "task_key": "Bronze_layer",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/Silver_layer/ERP/silver_erp_loc_a101.ipynb",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Silver_ERP_cat",
                "depends_on": [
                    {
                        "task_key": "Bronze_layer",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/Silver_layer/ERP/silver_erp_px_cat_g1v2",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Silver_crm_prd_info",
                "depends_on": [
                    {
                        "task_key": "Bronze_layer",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/Silver_layer/CRM/Silver_crm_prd_info",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Gold_Product_dimension",
                "depends_on": [
                    {
                        "task_key": "Silver_crm_prd_info",
                    },
                    {
                        "task_key": "Silver_ERP_cat",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/Gold_layer/gold_dim_products",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "silver_crm_sales_details",
                "depends_on": [
                    {
                        "task_key": "Bronze_layer",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/Silver_layer/CRM/silver_crm_sales_details",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Gold_fact_sales",
                "depends_on": [
                    {
                        "task_key": "silver_crm_sales_details",
                    },
                    {
                        "task_key": "Gold_Product_dimension",
                    },
                    {
                        "task_key": "Gold_Dim_customer",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/karishmaborse@gmail.com/DataBricks_2026/bike_lakehouse_1/Gold_layer/gold_fact_sales",
                    "source": "WORKSPACE",
                },
            },
        ],
        "queue": {
            "enabled": True,
        },
        "performance_target": "PERFORMANCE_OPTIMIZED",
    }
)

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
w.jobs.reset(new_settings=CRM_data_Ingestion, job_id=284437800891157)
# or create a new job using: w.jobs.create(**CRM_data_Ingestion.as_shallow_dict())
