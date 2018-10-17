# ARM Compozure
Automation tool to help manage ARM (Azure Resource Manager) template projects.

## Status
Early development, not yet usable.

## Setup
### Pre-requisites
 * Python
 * Pip
 * Virtualenv (optional)

### Build
1. Clone
```
git clone https://github.com/TimSwart/arm-compozure.git
```

2. If using Virtualenv (recommended)
```
virtualenv env
source env/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run tests
```
pytest
```

## TODO
1. Address import path issue in param_file.py
    - when running pytest, need to import ArmFile as:
    ```
     from src.arm_compozure.arm_file import ArmFile
    ```
    - when running python src/arm_compozure, need to import ArmFile as:
    ```
     from arm_file import ArmFile
    ```
