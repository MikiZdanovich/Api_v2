task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True

task_routes = {
    'tasks.add': 'low-priority',
}
