# wcm-io-devops.conga-host-facts

This role provides conga facts based on instance tags.

At the moment the following facts are retrieved:
* conga_node

## Requirements

This role requires Ansible 2.4.6 or higher.

### EC2 instance tags

The ec2 instances need the following tags to be set.

#### conga_nodes

Comma separated string containing all conga_node names of the host.

Example: `author-dev.website1.com,dev.website1.com`

####  conga_variants

Comma separated string containing all conga_variants of the host.

Example: `aem-author,aem-publish`

#### conga_variant_node_mapping

Comma separated string containing a mapping from conga_variant to conga_node.
Note: This mapping is only used on singlehost instances.

Example: `aem-author=author-dev.website1.com,aem-publish=dev.website1.com`

* conga_variant_node_mapping (comma separated string like: "")

### Static inventory variables

When not working with a ec2 inventory the host needs some variables to
be set.

Example:
```yaml
conga_roles:
  - aem-cms
  - aem-dispatcher

conga_variants:
  - aem-author
  - aem-publish

conga_nodes:
  - author.local-website1
  - local-website1

conga_variant_node_mapping:
    - "aem-author=author.local-website1"
    - "aem-publish=local-website1"

```

## Role Variables

    # conga_host_facts_pattern:

The ansible host pattern. This variable must be set!

    conga_host_facts_aws_region: "eu-west-1"

The aws region to use when facts are retrieved using ec2_instance_facts.

## Example

This playbook set the conga host facts for the hosts identified by the tasg
* Project = testproject
* Env = dev
* conga_variants = aem-author,aem-publish

```
- hosts: "&tag_Project_testproject:&tag_Env_dev:tag_conga_variants_aem-author:tag_conga_variants_aem-publish"
  pre_tasks:
    - name: Set conga host facts
      include_role:
        name: wcm-io-devops.conga-host-facts
      vars:
        conga_host_facts_pattern: "tag_conga_variants_aem-author"
```
