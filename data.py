import tools

level_key = tools.level_key


def course_title(title):
    # Decide level code
    for i in level_key:
        for j in level_key[i]:
            if j in title:
                return i
