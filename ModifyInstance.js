// ModifyEC2InstanceType


const AWS = require('aws-sdk');

exports.handler = (event, context, callback) => {
    const { instanceId, instanceRegion, instanceType } = event;
    
    const ec2 = new AWS.EC2({ region: instanceRegion });

//é um objeto usado para processamento assíncrono, representa um valor que pode estar disponível agora, no futuro ou nunca.
    Promise.resolve()
        .then(() => ec2.stopInstances({ InstanceIds: [instanceId] }).promise())
        .then(() => ec2.waitFor('instanceStopped', { InstanceIds: [instanceId] }).promise())
        .then(() => ec2.modifyInstanceAttribute({InstanceId: instanceId, InstanceType: { Value: instanceType } }).promise())
        .then(() => ec2.startInstances({ InstanceIds: [instanceId] }).promise())
        .then(() => callback(null, `Successfully modified ${event.instanceId} to ${event.instanceType}`))
        .catch(err => callback(err));
};




//{"region":"us-east-1", "instanceId": "", "instanceType":""}
