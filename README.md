# CloudShare Ansible Inventory

## Usage

`ansible -i cloudshare-inv.py all -m ping`

You can limit Ansible by environment:

`ansible -i cloudshare-inv.py my-env -m ping`

## Install

- Install the CloudShare Python SDK: `pip install cloudshare`.
- Download `cloudshare-inv.py`
- Define the following environment variables:
    - CLOUDSHARE_API_KEY
    - CLOUDSHARE_API_ID
    - You can find your API credentials [here](https://use.cloudshare.com/Ent/Vendor/UserDetails.aspx)


