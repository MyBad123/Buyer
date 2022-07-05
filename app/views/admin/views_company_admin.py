from django.shortcuts import render, redirect
from django.views import View
from app.models import Company


class AdminCompanyCreateSerializer:
    """methods for work with data in AdminCompanyCreate class"""

    def __init__(self):
        self.name = None

    def init_name(self, name):
        """initialize name"""

        self.name = name

    def control_name(self):
        """control name: valid or no; False == valid"""

        if type(self.name) != str:
            return True

        if self.name == '':
            return True

        return False

    def get_company_or_no(self):
        """control: db have company with name, or no"""

        if len(Company.objects.filter(name=self.name)):
            return False

        return True

    def save_name_to_db(self):
        """create company"""

        if self.get_company_or_no():
            Company.objects.create(name=self.name)


class AdminCompanyUpdateSerializer:
    """methods for work with data in AdminCompanyCreate class"""

    def __init__(self):
        self.name = None
        self.id = None

    def init_name(self, name, id):
        """initialize name"""

        self.name = name
        self.id = id

    def control(self):
        """control name: valid or no; False == valid"""

        # self.name: valid or no
        if type(self.name) != str:
            print(type(self.name))
            return True

        if self.name == '':
            return True

        # self.id: valid or no
        try:
            int(self.id)
        except ValueError:
            return True

        return False


class AdminCompaniesView(View):
    """class for getting all companies"""

    def get(self, request):
        """get all comapny"""

        if not request.user.is_superuser:
            return redirect('/user-page/')

        # make struct of data
        struct = []
        for i in Company.objects.all():
            struct.append({
                'name': i.name,
                'url': '/admin-update-company/?id=' + str(i.id)
            })

        return render(request, 'admin/companies.html', context={
            "companies": struct
        })


class AdminCompanyCreate(View, AdminCompanyCreateSerializer):
    """class for creating company"""

    def get(self, request):
        """get form for creating company"""

        if not request.user.is_superuser:
            return redirect('/user-page/')

        return render(request, 'admin/new_company.html')

    def post(self, request):
        """create company"""

        if not request.user.is_superuser:
            return redirect('/user-page/')

        # control: valid data or no
        super().init_name(
            name=request.POST.get('name')
        )
        if super().control_name():
            return redirect('/admin-create-company/')

        # save to db
        super().save_name_to_db()

        return redirect('/admin-create-company/')


class AdminUpdateCompanyView(View, AdminCompanyUpdateSerializer):
    """methods for update company"""

    def get(self, request):
        """get form for update company"""

        if not request.user.is_superuser:
            return redirect('/user-page/')

        # get company by id
        id_company = request.GET.get('id')
        try:
            company = Company.objects.get(id=id_company)
        except Company.DoesNotExist:
            return redirect('/admin-get-all-companies/')

        return render(request, 'admin/update_company.html', context={
            'name': company.name,
            'id': id_company
        })

    def post(self, request):
        """update company"""

        if not request.user.is_superuser:
            return redirect('/user-page/')

        # control: valid data or no
        super().init_name(
            name=request.POST.get('name', None),
            id=request.POST.get('id', None)
        )
        if super().control():
            return redirect('/admin-update-company/')

        # update company
        try:
            company = Company.objects.get(id=int(request.POST.get('id')))
            company.name = request.POST.get('name')
            company.save()
        except Company.DoesNotExist:
            return redirect('/admin-update-company/')

        return redirect('/admin-update-company/?id=' + str(request.POST.get('id')))
