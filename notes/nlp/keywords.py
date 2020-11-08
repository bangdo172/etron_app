
CANCEL_WORDS = ['xoá', 'huỷ', 'không cần']

CHECK_WORDS = ['xong', 'đã']

EDIT_WORDS = ['thay đổi', 'hoãn', 'đổi', 'chuyển', 'rời']

UPDATE_WORDS = CANCEL_WORDS + CHECK_WORDS + EDIT_WORDS

REMIND_WORDS = ['nhắc tôi']

ASK_WORDS = [('when:when', 'start_time'), ('where:where', 'location'), ('what:what', '*')]

OBJECT_WORDS = ['wit$contact:contact', 'organization:organization', 'wit$location:location']

PRIORITY_KEY ='priority:priority'
TIME_KEY = 'wit$datetime:datetime'
