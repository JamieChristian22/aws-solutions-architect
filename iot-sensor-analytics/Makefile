.PHONY: bootstrap deploy destroy synth diff

CDK_DIR=cdk
VENV=$(CDK_DIR)/.venv

$(VENV):
\tpython -m venv $(VENV)
\t. $(VENV)/bin/activate && pip install -r $(CDK_DIR)/requirements.txt && npm i -g aws-cdk@2

bootstrap: | $(VENV)
\t. $(VENV)/bin/activate && cdk bootstrap

deploy: | $(VENV)
\t. $(VENV)/bin/activate && cdk deploy --require-approval never

destroy: | $(VENV)
\t. $(VENV)/bin/activate && cdk destroy --force

synth: | $(VENV)
\t. $(VENV)/bin/activate && cdk synth

diff: | $(VENV)
\t. $(VENV)/bin/activate && cdk diff
