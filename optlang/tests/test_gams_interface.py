# Copyright (c) 2013 Novo Nordisk Foundation Center for Biosustainability, DTU.
# See LICENSE for details.
import copy

import unittest
import random
import pickle

import os
import nose
import six

from optlang import glpk_interface
from optlang.gams_interface import Variable, Constraint, Objective, Model
from optlang import gams_interface
from optlang.util import glpk_read_cplex

from optlang.tests import abstract_test_cases


random.seed(666)
TESTMODELPATH = os.path.join(os.path.dirname(__file__), 'data/model.lp')
TESTMILPMODELPATH = os.path.join(os.path.dirname(__file__), 'data/simple_milp.lp')

def read_test_model():
    model = glpk_interface.Model(problem=glpk_read_cplex(TESTMODELPATH))
    model = Model.clone(model)
    return model


class VariableTestCase(abstract_test_cases.AbstractVariableTestCase):
    interface = gams_interface

    def test_get_primal(self):
        self.assertEqual(self.var.primal, None)
        model = read_test_model()
        model.optimize()
        for i, j in zip([var.primal for var in model.variables], [0.8739215069684306, -16.023526143167608, 16.023526143167604, -14.71613956874283, 14.71613956874283, 4.959984944574658, 4.959984944574657, 4.959984944574658, 3.1162689467973905e-29, 2.926716099010601e-29, 0.0, 0.0, -6.112235045340358e-30, -5.6659435396316186e-30, 0.0, -4.922925402711085e-29, 0.0, 9.282532599166613, 0.0, 6.00724957535033, 6.007249575350331, 6.00724957535033, -5.064375661482091, 1.7581774441067828, 0.0, 7.477381962160285, 0.0, 0.22346172933182767, 45.514009774517454, 8.39, 0.0, 6.007249575350331, 0.0, -4.541857463865631, 0.0, 5.064375661482091, 0.0, 0.0, 2.504309470368734, 0.0, 0.0, -22.809833310204958, 22.809833310204958, 7.477381962160285, 7.477381962160285, 1.1814980932459636, 1.496983757261567, -0.0, 0.0, 4.860861146496815, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.064375661482091, 0.0, 5.064375661482091, 0.0, 0.0, 1.496983757261567, 10.000000000000002, -10.0, 0.0, 0.0, 0.0, 0.0, 0.0, -29.175827135565804, 43.598985311997524, 29.175827135565804, 0.0, 0.0, 0.0, -1.2332237321082153e-29, 3.2148950476847613, 38.53460965051542, 5.064375661482091, 0.0, -1.2812714099825612e-29, -1.1331887079263237e-29, 17.530865429786694, 0.0, 0.0, 0.0, 4.765319193197458, -4.765319193197457, 21.79949265599876, -21.79949265599876, -3.2148950476847613, 0.0, -2.281503094067127, 2.6784818505075303, 0.0]):
            self.assertAlmostEqual(i, j)

    def test_get_dual(self):
        self.assertEqual(self.var.dual, None)
        model = read_test_model()
        model.optimize()
        print(list(var.dual for var in model.variables))
        for i, j in zip([var.dual for var in model.variables], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.022916186593776228, 0.0, 0.0, 0.0, -0.03437427989066433, 0.0, -0.007638728864592069, 0.0, -0.0012731214774320057, 0.0, 0.0, 0.0, 0.0, 0.0, -0.005092485909728044, 0.0, 0.0, 0.0, 0.0, -0.005092485909728045, 0.0, 0.0, -0.005092485909728052, 0.0, 0.0, 0.0, -0.06110983091673658, -0.00509248590972803, 0.0, -0.003819364432296038, -0.0050924859097280575, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.03946676580039237, 0.0, 0.0, -0.0050924859097280385, 0.0, -0.0012731214774320113, 0.0, -0.09166474637510488, 0.0, 0.0, 0.0, 0.0, -0.04583237318755244, 0.0, 0.0, -0.09166474637510488, -0.005092485909728051, -0.07002168125876067, 0.0, -0.06874855978132866, 0.0, 0.0, 0.0, 0.0, -0.0012731214774320022, -0.003819364432296038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.040739887277824384, -0.04583237318755244, -0.0012731214774320205, 0.0, 0.0, 0.0, 0.0, 0.0, -0.03437427989066433, 0.0, 0.0, -0.04837861614241647]):
            self.assertAlmostEqual(i, j)

    def test_setting_lower_bound_higher_than_upper_bound_raises(self):
        model = read_test_model()
        model.optimize()
        self.assertRaises(ValueError, setattr, model.variables[0], 'lb', 10000000000.)

    def test_setting_nonnumerical_bounds_raises(self):
        model = read_test_model()
        self.assertRaises(Exception, setattr, model.variables[0], 'lb', 'Chicken soup')

    def test_changing_variable_names_is_reflected_in_the_solver(self):
        model = read_test_model()
        for i, variable in enumerate(model.variables):
            variable.name = "var"+str(i)
            self.assertEqual(variable.name, "var"+str(i))


class ConstraintTestCase(abstract_test_cases.AbstractConstraintTestCase):
    interface = gams_interface

    def test_get_primal(self):
        self.assertEqual(self.constraint.primal, None)
        self.model.optimize()
        print([constraint.primal for constraint in self.model.constraints])
        for i, j in zip([constraint.primal for constraint in self.model.constraints], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.048900234729145e-15, 0.0, 0.0, 0.0, -3.55971196577979e-16, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.5546369406238147e-17, 0.0, -5.080374405378186e-29, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
            self.assertAlmostEqual(i, j)

    # def test_get_dual(self):
    #     self.assertEqual(self.constraint.dual, None)
    #     self.model.optimize()
    #     for i, j in zip([constraint.dual for constraint in self.model.constraints], [-0.047105494664984454, -0.042013008755256424, -0.04201300875525642, -0.09166474637510488, -0.09039162489767284, -0.024189308071208247, -0.022916186593776238, -0.03437427989066435, -0.03437427989066435, -0.028008672503504285, -0.07129480273619271, -0.029281793980936298, 0.005092485909728047, -0.06238295239416862, -0.06110983091673661, 0.010184971819456094, 0.0, -0.07129480273619271, -5.140926862910144e-32, -6.0634800261074814e-33, 0.0, -0.052197980574712505, -0.06747543830389666, -0.040739887277824405, -0.03946676580039239, -0.09803035376226496, -0.10439596114942501, 0.0, 0.0, -0.0916647463751049, -0.04837861614241648, -0.04583237318755246, -0.052197980574712505, -0.09803035376226495, -0.0916647463751049, -0.07511416716848872, -0.07002168125876067, -0.07002168125876068, -0.06874855978132868, -0.019096822161480186, -1.5662469903861418e-32, -0.0, 0.0012731214774320113, -0.0, -0.07129480273619271, -0.04201300875525642, -0.04073988727782441, -0.048378616142416474, -0.04583237318755245, 0.0, -0.00763872886459207, 0.0, -0.008911850342024085, -0.0, -0.0, -0.0, -0.0, -0.042013008755256424, -0.042013008755256424, -0.0012731214774320118, -0.0, -0.035647401368096354, -0.03437427989066435, 0.002546242954864023, 0.0, -0.08275289603308078, -0.0827528960330808, -0.11330781149144908, -0.050924859097280506, -0.04837861614241648, -0.05474422352957655, -0.08275289603308081]):
    #         self.assertAlmostEqual(i, j)

    def test_change_constraint_name(self):
        constraint = copy.copy(self.constraint)
        self.assertEqual(constraint.name, 'woodchips')
        constraint.name = 'ketchup'
        self.assertEqual(constraint.name, 'ketchup')
        self.assertEqual([constraint.name for constraint in self.model.constraints], ['M_13dpg_c', 'M_2pg_c', 'M_3pg_c', 'M_6pgc_c', 'M_6pgl_c', 'M_ac_c', 'M_ac_e', 'M_acald_c', 'M_acald_e', 'M_accoa_c', 'M_acon_C_c', 'M_actp_c', 'M_adp_c', 'M_akg_c', 'M_akg_e', 'M_amp_c', 'M_atp_c', 'M_cit_c', 'M_co2_c', 'M_co2_e', 'M_coa_c', 'M_dhap_c', 'M_e4p_c', 'M_etoh_c', 'M_etoh_e', 'M_f6p_c', 'M_fdp_c', 'M_for_c', 'M_for_e', 'M_fru_e', 'M_fum_c', 'M_fum_e', 'M_g3p_c', 'M_g6p_c', 'M_glc_D_e', 'M_gln_L_c', 'M_gln_L_e', 'M_glu_L_c', 'M_glu_L_e', 'M_glx_c', 'M_h2o_c', 'M_h2o_e', 'M_h_c', 'M_h_e', 'M_icit_c', 'M_lac_D_c', 'M_lac_D_e', 'M_mal_L_c', 'M_mal_L_e', 'M_nad_c', 'M_nadh_c', 'M_nadp_c', 'M_nadph_c', 'M_nh4_c', 'M_nh4_e', 'M_o2_c', 'M_o2_e', 'M_oaa_c', 'M_pep_c', 'M_pi_c', 'M_pi_e', 'M_pyr_c', 'M_pyr_e', 'M_q8_c', 'M_q8h2_c', 'M_r5p_c', 'M_ru5p_D_c', 'M_s7p_c', 'M_succ_c', 'M_succ_e', 'M_succoa_c', 'M_xu5p_D_c']
)
        for i, constraint in enumerate(self.model.constraints):
            constraint.name = 'c'+ str(i)
        self.assertEqual([constraint.name for constraint in self.model.constraints], ['c' + str(i) for i in range(0, len(self.model.constraints))])

    def test_setting_lower_bound_higher_than_upper_bound_raises(self):
        model = self.model
        self.assertRaises(ValueError, setattr, model.constraints[0], 'lb', 10000000000.)

    def test_setting_nonnumerical_bounds_raises(self):
        model = self.model
        self.assertRaises(Exception, setattr, model.constraints[0], 'lb', 'Chicken soup')


class ModelTestCase(abstract_test_cases.AbstractModelTestCase):
    interface = gams_interface

    def test_pickle_ability(self):
        self.model.optimize()
        value = self.model.objective.value
        pickle_string = pickle.dumps(self.model)
        from_pickle = pickle.loads(pickle_string)
        from_pickle.optimize()
        self.assertAlmostEqual(value, from_pickle.objective.value)
        self.assertEqual([(var.lb, var.ub, var.name, var.type) for var in from_pickle.variables.values()],
                         [(var.lb, var.ub, var.name, var.type) for var in self.model.variables.values()])
        self.assertEqual([(constr.lb, constr.ub, constr.name) for constr in from_pickle.constraints],
                         [(constr.lb, constr.ub, constr.name) for constr in self.model.constraints])

    def test_config_gets_copied_too(self):
        self.assertEquals(self.model.configuration.verbosity, 0)
        self.model.configuration.verbosity = 3
        model_copy = copy.copy(self.model)
        self.assertEquals(model_copy.configuration.verbosity, 3)

    def test_add_non_cplex_conform_variable(self):
        var = Variable('12x!!@#5_3', lb=-666, ub=666)
        self.model.add(var)
        self.assertTrue(var in self.model.variables.values())
        self.assertEqual(self.model.variables['12x!!@#5_3'].lb, -666)
        self.assertEqual(self.model.variables['12x!!@#5_3'].ub, 666)
        repickled = pickle.loads(pickle.dumps(self.model))
        var_from_pickle = repickled.variables['12x!!@#5_3']

    def test_change_of_constraint_is_reflected_in_low_level_solver(self):
        x = Variable('x', lb=-83.3, ub=1324422.)
        y = Variable('y', lb=-181133.3, ub=12000.)
        constraint = Constraint(0.3 * x + 0.4 * y, lb=-100, name='test')
        self.assertEqual(constraint.index, None)
        self.model.add(constraint)
        self.assertEqual(self.model.constraints['test'].__str__(), 'test: -100 <= 0.4*y + 0.3*x')
        self.assertEqual(constraint.index, 73)
        z = Variable('z', lb=3, ub=10, type='integer')
        self.assertEqual(z.index, None)
        constraint += 77. * z
        self.assertEqual(z.index, 98)
        self.assertEqual(self.model.constraints['test'].__str__(), 'test: -100 <= 0.4*y + 0.3*x + 77.0*z')
        print(self.model)
        self.assertEqual(constraint.index, 73)

    def test_change_of_objective_is_reflected_in_low_level_solver(self):
        x = Variable('x', lb=-83.3, ub=1324422.)
        y = Variable('y', lb=-181133.3, ub=12000.)
        objective = Objective(0.3 * x + 0.4 * y, name='test', direction='max')
        self.model.objective = objective
        self.assertEqual(self.model.objective.__str__(), 'Maximize\n0.4*y + 0.3*x')
        z = Variable('z', lb=4, ub=4, type='integer')
        self.model.objective += 77. * z
        self.assertEqual(self.model.objective.__str__(), 'Maximize\n0.4*y + 0.3*x + 77.0*z')

    @unittest.skip('Skipping for now')
    def test_absolute_value_objective(self):
        # TODO: implement hack mentioned in http://www.aimms.com/aimms/download/manuals/aimms3om_linearprogrammingtricks.pdf

        objective = Objective(sum(abs(variable) for variable in six.itervalues(self.model.variables)), name='test',
                              direction='max')
        print(objective)
        self.assertTrue(False)

    def test_initial_objective(self):
        self.assertEqual(self.model.objective.expression.__str__(), '1.0*R_Biomass_Ecoli_core_w_GAM')

    def test_raise_on_non_linear_objective(self):
        """Test that an exception is raised when a non-linear objective is added to the model."""
        v1, v2 = self.model.variables.values()[0:2]
        self.assertRaises(ValueError, Objective, v1*v2)

    def test_set_copied_objective(self):
        obj_copy = copy.copy(self.model.objective)
        self.model.objective = obj_copy
        self.assertEqual(self.model.objective.__str__(), 'Maximize\n1.0*R_Biomass_Ecoli_core_w_GAM')

    def test_timeout(self):
        self.model.configuration.timeout = 0
        status = self.model.optimize()
        self.assertEqual(status, 'time_limit')

    def test_set_linear_coefficients_objective(self):
        1 / 0
        # self.model._set_linear_objective_term(self.model.variables.R_TPI, 666.)
        # self.assertEqual(glp_get_obj_coef(self.model.problem, self.model.variables.R_TPI.index), 666.)

    def test_primal_values(self):
            self.model.optimize()
            for k, v in self.model.primal_values.items():
                self.assertEquals(v, self.model.variables[k].primal)

    def test_reduced_costs(self):
        self.model.optimize()
        for k, v in self.model.reduced_costs.items():
            self.assertEquals(v, self.model.variables[k].dual)

    def test_dual_values(self):
        self.model.optimize()
        for k, v in self.model.dual_values.items():
            self.assertEquals(v, self.model.constraints[k].primal)

    def test_shadow_prices(self):
        self.model.optimize()
        for k, v in self.model.shadow_prices.items():
            self.assertEquals(v, self.model.constraints[k].dual)

    def test_change_constraint_bounds(self):
        1 / 0

    def test_change_variable_bounds(self):
        1 / 0

    def test_constraint_set_problem_to_None_caches_the_latest_expression_from_solver_instance(self):
        1 / 0

    def test_iadd_objective(self):
        1 / 0

    def test_imul_objective(self):
        1 / 0

    def test_init_from_existing_problem(self):
        1 / 0

    def test_set_linear_coefficients_constraint(self):
        1 / 0



if __name__ == '__main__':
    nose.runmodule()