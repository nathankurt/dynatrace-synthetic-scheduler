Example usage:
  python3 syntheticscheduler.py --tags 24x7,Weekend --enabled True
    - This will enable a Synthetic script that has the tags: APIManaged, 24x7, Weekend

  python3 syntheticscheduler.py --tags 24x7,Weekend --enabled False
    - This will disable a Synthetic script that has the tags: APIManaged, 24x7, Weekend

Use a crontab for for specifying when scripts with certain tags should be enabled/disabled.

Synthetic transactions need atleast 1 tag: APIManaged.

You can specify additional tags with the "--tags tag1,tag2,tag3" command-line option.
