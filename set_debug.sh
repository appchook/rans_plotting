#/bin/bash
echo "Setting logging level to debug..."
sed -i 's/logger name="\*" minlevel="Info" writeTo="file"/logger name="\*" minlevel="Debug" writeTo="file"/g' /var/data/zerto/zvr/zvm/nlog.config
echo "deleteting ZVM pod..."
kubectl delete pod --selector=appService=zvm-service
