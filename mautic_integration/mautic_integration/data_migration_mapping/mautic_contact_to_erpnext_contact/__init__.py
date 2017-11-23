def pre_process(contacts):
	return {
		'id': contacts["id"],
		'firstname': contacts["fields"]["all"]["firstname"],
		'lastname': contacts["fields"]["all"]["lastname"],
		'email': contacts["fields"]["all"]["email"]
	}
