import time
import boto3

instance_states = {'start':('stopping','stopped'),'stop':('pending','running')}

def action_instance_handler(event, context):
	action = event['action']
	ec2 = boto3.resource('ec2', region_name=event['region'])

	instance = ec2.Instance(event['instance_id'])
	if instance.state['Name'] in ('shutting-down','terminated'):
		print('Instance %s - %s' % (instance.id, instance.state))
	elif instance.state['Name'] in instance_states[action]:
		while instance.state['Name'] != instance_states[action][1]:
			time.sleep(10)
			instance.reload()
			print('Instance %s is %s' % (instance.id, instance_states[action][0]))
		if action == 'start':
			print('Starting Instance %s - Initiated' % (instance.id))
			instance.start()
			while instance.state['Name'] != 'running':
				time.sleep(10)
				instance.reload()
				print('Instance %s is starting' % (instance.id))
			print('Starting Instance %s  - Finished' % (instance.id))
		elif action == 'stop':
			print('Stopping Instance %s - Initiated' % (instance.id))
			instance.stop()
			while instance.state['Name'] != 'stopped':
				time.sleep(10)
				instance.reload()
				print('Instance %s is stopping' % (instance.id))
			print('Stopping Instance %s  - Finished' % (instance.id))
	else:
		print('Instance %s already %s' % (instance.id, instance.state['Name']))
		
		
		
		
		#cloudwatch rule {"region":"us-east-1", "action": "start", "instance_id":""}
                 #{"region":"us-east-1", "action": "stop", "instance_id":""}
