# wcm_io_devops.conga_host_facts

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

An example can be found below [tests](tests). The tests use the
[conga-aem-definitions](https://github.com/wcm-io-devops/conga-aem-definitions)
as CONGA configuration.

The playbook [test-singlehost.yml](tests/test-singlehost.yml) will
retrieve the `conga_node` based on the `host_pattern` provided in the
two `include_playbook` statements.

The playbook [test-multihost.yml](tests/test-multihost.yml) will
retrieve the `conga_node` based on the `host_pattern` with the value
`aem-author:aem-publish`.

Both variants include the playbook
[include-test.yml](tests/include-test.yml) which applies the
wcm_io_devops.conga_host_facts role, followed by the
wcm_io_devops.conga_facts role to retrieve the conga configuration for
the node, role and variant.

Please refer to the [host_vars](tests/host_vars) and the
[inventory](tests/inventory) files on how to configure both setups.