az container create --resource-group appsvc_linux_centralus_basic `
  --name flasktesting-container `
  --image flasktesting.azurecr.io/flask-langflow-app:latest `
  --dns-name-label flasktesting-langflow `
  --ports 8000 `
  --registry-login-server flasktesting.azurecr.io `
  --registry-username flasktesting `
  --registry-password Gmt0W4XLFFMKcrAHJbTnp1PghaSMSI5PleImypMcMK+ACRBnZMgl `
  --os-type Linux `
  --cpu 1 `
  --memory 1.5

  curl -X POST "http://flask-langflow.centralus.azurecontainer.io:8000/chat" \         
   -H "Content-Type: application/json" \
   -d '{"message": "Hello, how are you?"}'


  az container show --resource-group appsvc_linux_centralus_basic --name flasklangflow-container --query ipAddress.fqdn

  flasktesting.azurecr.io/flask-langflow-app