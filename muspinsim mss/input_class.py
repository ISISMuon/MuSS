'''
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: August 2023

Summary:
Class that creates the file to be parsed by the MuSpinInput
this is important because we are associating variables with an object in this class

'''
from ase import io


class Create_Input:
    def __init__(self, input, name='Example', spins='mu', cif=False, time='range(0, 0.1, 100)', polarization=None, field=None, intrisic_field=None,
                 x_axis=None, y_axis=None, average_axes=None,
                 orientation=None, temperature=None, fitting_variables=None, fitting_data=None, fitting_method=None,
                 fitting_tolerance=None, experiment=None, zeeman=None, hyperfine=None, dipolar=None,
                 quadripolar=None, dissipation=None, celio=None):
        self.input = input
        self.name = name
        self.spins = spins
        self.cif = cif
        self.polarization = polarization
        self.field = field
        self.intrisic_field = intrisic_field
        self.times = time
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.average_axes = average_axes
        self.orientation = orientation
        self.temperature = temperature
        self.fitting_variables = fitting_variables
        self.fitting_data = fitting_data
        self.fitting_method = fitting_method
        self.fitting_tolerance = fitting_tolerance
        self.experiment = experiment
        self.zeeman = zeeman
        self.hyperfine = hyperfine
        self.dipolar = dipolar
        self.quadripolar = quadripolar
        self.dissipation = dissipation
        self.celio = celio

    def __call__(self, path=None, position_mu=[0, 0, 0]):
        '''when the object of the class has been created it can be call
        when is called if cif=True the path of the cif file must be passed'''
        with open(self.input, 'w') as f:
            # f.write('name \n    {0} \nspins\n   {1} '.format(self.name,self.spins))
            if self.cif == True:
                if path == None:
                    raise Exception(
                        'When self.cif =True path of the cif file must be given')
                self.cif_files(path, position_mu, f)

            self.write(f)

    def __str__(self) -> str:

        pass

    def write(self, f):
        '''Here the parameters correspond to a string which is what is being written 
        in the file
        This could be done more efficiently with a dictionary maybe'''

        list_of_parameters = [self.name, self.spins, self.times, self.polarization, self.field, self.intrisic_field, self.x_axis,
                              self.y_axis, self.average_axes, self.orientation, self.temperature, self.fitting_variables, self.fitting_data,
                              self.fitting_method, self.fitting_tolerance, self.experiment, self.zeeman, self.hyperfine, self.dipolar, self.quadripolar,
                              self.dissipation, self.celio]

        list_of_variables = ['name', 'spins', 'time', 'polarization', 'field', 'intrisic_field', 'x_axis',
                             'y_axis', 'average_axes', 'orientation', 'temperature', 'fitting_variables', 'fitting_data',
                             'fitting_method', 'fitting_tolerance', 'experiment', 'zeeman', 'hyperfine', 'dipolar', 'quadripolar',
                             'self.dissipation', 'celio']
        n = 0
        for i in list_of_parameters:

            if i != None and i != '':
                if n == 0:
                    f.write('{0}\n   {1}\n'.format(list_of_variables[n], i))
                else:
                    # print(list_of_variables[n],i)
                    f.write('\n{0}\n   {1}\n'.format(list_of_variables[n], i))
            n += 1

    def cif_files(self, path, position_mu, f):
        ''' Here the path of the cif file is given
        and the calcutaion of the muon relative to cif file is done

        Note**
        This is made specifically for dipolar interaction
        '''
        read_doc = io.read(path)
        position = read_doc.get_positions()
        reltv_position = []
        for i in position:
            i = i+position_mu
            reltv_position.append(i)

        for j in read_doc.get_chemical_symbols():
            f.write(' {0} '.format(j))
            number = 0
        for i in reltv_position:
            print(number)
            print('I am i in anna', i)
            f.write('\ndipolar 1 {0}\n   '.format(number+2))
            f.write('')
            number += 1
            for ii in i:
                f.write(str(ii))
                f.write(' ')
            f.writelines('\n')

    # Self contained version of cif_file
    # where the file is read with th intention to append cif file info
    def cif_filee(self, path, position_mu):
        # Self contained version of cif_file
        read_doc = io.read(path)
        position = read_doc.get_positions()
        reltv_position = []
        for i in position:
            i = i+position_mu
            reltv_position.append(i)

        with open(self.input, 'a+') as f:
            # f.write(' {0} \n spins \n    {1} '.format(self.name))
            for j in read_doc.get_chemical_symbols():
                f.write(' {0} '.format(j))
            number = 0
            for i in reltv_position:
                print(number)
                print('I am i in anna', i)
                f.write('\n dipolar 1 {0}\n   '.format(number+2))
                f.write('')
                number += 1
                for ii in i:
                    f.write(str(ii))
                    f.write(' ')
                f.writelines('\n')


'''Test the object created by Create_Input_Class'''
inn = Create_Input(
    r'C:\Users\BNW71814\Desktop\GUI for InputMuspinSim\examplessss.txt', 'oooooo', 'mu', cif=False)


inn.name = 'francezinha'
