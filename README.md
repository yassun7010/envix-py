# Simple Secret Injector CLI tool

[![pypi package](https://badge.fury.io/py/envix.svg)](https://pypi.org/project/envix)


## Usage

```sh
cat > envix.yaml <<EOF
envix:
  version: 1

envs:
  - type: Raw
    items:
      MY_SECRET: '!!!secret!!!!'
EOF

envix inject --clear-environments -- env
```
