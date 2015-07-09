#coding=utf-8

#当前视频的前一个或者下一个视频的实例
def get_vid_for_direction(instance, direction):
	''' get next video instance based on direction and current video instance'''
	#当前视频属于哪一个分类
	category = instance.category
	#当前视频分类中的所有视频
	video_qs = category.video_set.all()
	if direction == "next":
		#当前视频在数组中的下一个视频，order__gt=Greater than
		new_qs = video_qs.filter(order__gt=instance.order)
	else:
		#当前视频在数组中的前一个视频，order__lt=Litter than
		new_qs = video_qs.filter(order__lt=instance.order).reverse()
	next_vid = None
	#如果当前分类中的视频大于等于一个
	if len(new_qs) >= 1:
		try:
			next_vid = new_qs[0]
		except IndexError:
			next_vid = None
	return next_vid
