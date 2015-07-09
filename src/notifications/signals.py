from django.dispatch import Signal


notify = Signal(providing_args=['recipient', 'verb', 'action', 'target', 'affected_users'])


#notify_reply = Signal(providing_args=['recipient', 'comment', 'action'])



# notify.send(
# 						request.user, 
# 						action=new_comment, 
# 						target=parent_comment, 
# 						recipient=parent_comment.user, 
# 						verb='replied to')