#-*-encoding:utf-8-*-

PROFILE_DEV = 10
PROFILE_TEST = 20
PROFILE_TEST_ONLINE = 30
PROFILE_PRODUCT = 100


class Profile:
    def __init__(self):
        self.current_profile = PROFILE_DEV
        pass

    def set_profile(self, profile):
        if profile:
            self.current_profile = profile

    def get_profile(self):
        return self.current_profile


profile = Profile()








