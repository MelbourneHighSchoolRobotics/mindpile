from mindpile.Mapping.utils import MethodCall, Requires, Setup

@Setup
def ev3sim_setup():
  return '''
    import ev3sim.code_helpers
  '''

@MethodCall(target="ev3sim_wait_for_tick.vix")
@Requires(ev3sim_setup)
def wait_for_tick():
  return '''
    ev3sim.code_helpers.wait_for_tick()
  '''
