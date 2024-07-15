'''
Johnny's code on muo enviroments
'''
from ase import atoms, atom, build
import copy
import numpy as np
import ase
from ase.visualize import view


def make_supercell(atoms_mu: atoms, unperturbed_atoms: atoms = None, unperturbed_supercell=1,
                   small_output=False):
    """
    make a supercell with atoms_mu in the centre, and surrounded by unperturbed_supercell unperturbed_atoms
    :param atoms_mu: ASE atoms, maybe with distortions, including muon
    :param unperturbed_atoms: ASE atoms of unperturbed structure
    :param unperturbed_supercell: number of instances of unperturbed_atoms to bolt on to the end of atoms_mu
    :return: supercell of atoms_mu+unperturbed_supercell*unperturbed_atoms. If small_output==False, return ASE atoms,
             otherwise returns a list of [atom type, position]
    """

    # make the supercell structure
    # the changes are not stressing the orginal atom
    atoms_mu = copy.deepcopy(atoms_mu)
    view(atoms_mu)
    print('this is the atom we out in and deep copy', atoms_mu)
    if unperturbed_atoms is None:
        unperturbed_atoms = copy.deepcopy(atoms_mu[:-1])
        print(atoms_mu[:-1])
        view(atoms_mu)
    else:
        unperturbed_atoms = copy.deepcopy(unperturbed_atoms)
    # if atoms_mu is already a supercell, then make unperturbed_atoms a supercell of the same size

    unperturbed_atoms = build.make_supercell(unperturbed_atoms, np.diag([1, 1, 1]) *
                                             atoms_mu.cell.lengths()[0] /
                                             unperturbed_atoms.cell.lengths()[0], wrap=False)
    muon = copy.deepcopy(atoms_mu[-1])
    # view(muon)
    print(muon)
    output_list = []
    if small_output:
        output_list = [[this_atom.symbol, this_atom.position]
                       for this_atom in atoms_mu]

    del atoms_mu[-1]

    # we do the geometry of the supercell
    for x_sign in range(-unperturbed_supercell, unperturbed_supercell + 1):
        for y_sign in range(-unperturbed_supercell, unperturbed_supercell + 1):
            for z_sign in range(-unperturbed_supercell, unperturbed_supercell + 1):
                if x_sign == y_sign == z_sign == 0:
                    continue
                translation_vector = np.sign(x_sign) * (abs(x_sign) - 1) * unperturbed_atoms.cell[0] + \
                    np.sign(x_sign) * atoms_mu.cell[0]
                translation_vector += np.sign(y_sign) * (abs(y_sign) - 1) * unperturbed_atoms.cell[1] + \
                    np.sign(y_sign) * atoms_mu.cell[1]
                translation_vector += np.sign(z_sign) * (abs(z_sign) - 1) * unperturbed_atoms.cell[2] + \
                    np.sign(z_sign) * atoms_mu.cell[2]
                unperturbed_atoms.translate(translation_vector)
                for this_atom in unperturbed_atoms:
                    if small_output:
                        output_list.append(
                            [this_atom.symbol, copy.deepcopy(this_atom.position)])
                    else:
                        atoms_mu.append(this_atom)
                unperturbed_atoms.translate(-1 * translation_vector)

    atoms_mu.append(muon)

    if small_output:
        return output_list
    else:
        old_cell = atoms_mu.get_cell()
        atoms_mu.set_cell(
            old_cell*(2*unperturbed_supercell + 1), scale_atoms=False)
        atoms_mu.translate(unperturbed_supercell * old_cell[0])
        atoms_mu.translate(unperturbed_supercell * old_cell[1])
        atoms_mu.translate(unperturbed_supercell * old_cell[2])
        print('final atoms', atoms_mu)
        view(atoms_mu)
        return atoms_mu


file = ase.io.read(r'c:\Users\BNW71814\Desktop\EntryWithCollCode60559.cif')

# print(make_supercell(file))
# make_supercell(file)


######################################################################################################## One More Function #######################################################


def add_muon_to_aseatoms(ase_atoms: atoms, theta: float = 180, phi: float = 0, nn_indices: list = None,
                         muon_position: np.ndarray = None, plane_atom_index: int = None,
                         plane_atom_position: np.ndarray = None, midpoint=0.5) -> atoms:
    """
    adds a muon to ase_atoms
    :param ase_atoms: ASE atoms of the crystal the muon is going to be placed into
    :param theta: F--mu--F angle in degrees. Must also define nn_indices if this is not 180deg.
    :param phi: angle of the F--mu--F plane. Must also define theta and nn_indices to use this.
    :param nn_indices: ASE index of the nearest-neighbour atoms to place the muon in between. Do not define this AND
                       muon_position
    :param muon_position: position of the muon, in angstroms. Use EITHER this or nn_indices. Do not define this and
                          theta and phi
    :param plane_atom_index: index of atom which the muon moves away from to create the angle theta. Do not define this
                             and plane_atom_position.
    :param plane_atom_position: np array of position of the plane_atom (doesn't actually need to be a position of an
                                atom per se, but useful if it is. Do not define this and the index.
    :param midpoint: weighting of the midpoint to the two nnindices. 0 puts the muon on nn_indices[0], 1 puts it on
                     nn_indices[2]. 0.5 puts it in between the two.
    :return: ase_atoms with the muon
    """

    # check either muon_position xor nn_indices is None
    assert (muon_position is None) != (nn_indices is None)

    ase_atoms = copy.deepcopy(ase_atoms)

    # three possibilities:
    # 1) >2 nn_indices -> just find average, ignore angles
    # 2) 2 nn_indices or muon_position, theta not given (or 180) -> just find midpoint
    # 3) 2 nn_indices, theta and phi -- find muon_position using theta and phi

    # see how many nn_indices there are
    if nn_indices is not None:
        muon_position = np.zeros((3,))
        # possibility 1 (or 2)
        if len(nn_indices) > 2:
            # if nn_indices are given, work out the average of them to get the muon position (there can be more than 2!)
            for nn_index in nn_indices:
                muon_position += ase_atoms[nn_index].position / len(nn_indices)
        elif (len(nn_indices) == 2 and (theta == 180 or theta is None)):
            muon_position = ase_atoms[nn_indices[0]].position * midpoint \
                + ase_atoms[nn_indices[1]].position*(1-midpoint)
        elif len(nn_indices) == 2:
            # we need to calculate the muon position with theta and phi...

            # convert everything into TCoord3D objects (...easier to work with)
            nn_position_1 = ase_atoms[nn_indices[0]].position
            # nn_position_1 = coord(nn_position_1[0], nn_position_1[1], nn_position_1[2])
            nn_position_2 = ase_atoms[nn_indices[1]].position
            # nn_position_2 = coord(nn_position_2[0], nn_position_2[1], nn_position_2[2])

            # check the plane atom has been defined
            assert (plane_atom_index is None) != (plane_atom_position is None)

            if plane_atom_position is None:
                plane_atom_position = ase_atoms[plane_atom_index].position
            # plane_atom_position_c = coord(plane_atom_position[0], plane_atom_position[1], plane_atom_position[2])

            # muon_position = get_bent_muon_position(nn_position_1=nn_position_1, nn_position_2=nn_position_2,plane_position=plane_atom_position_c, theta=theta, phi=phi,midpoint=midpoint)

            muon_position = muon_position.tonumpyarray()

        else:
            print('Error with the muon position parameters.')
            assert False

    # now add the muon to the ASE atoms
    muon = atom.Atom('X', position=muon_position)
    print(muon)
    ase_atoms.append(muon)

    return ase_atoms
