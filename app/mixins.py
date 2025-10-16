from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

class AstronomerRequiredMixin(UserPassesTestMixin):
    def testFunc(self):
        return self.request.user.is_authenticated and self.request.user.type == 'astronomer'
    
    def handleNoPermission(self):
        messages.error(self.request, 'You must be an astronomer to access this page.')

        return redirect('home')
