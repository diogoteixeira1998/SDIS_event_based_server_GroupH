
class Request:
  def __init__(self, request_id, request_state, connection, search_val, result_db1, result_db2, t_begin, t_finish, t_thread1, t_thread2,
               t_thread3):
    self.request_id = request_id
    self.request_state = request_state
    self.connection = connection
    self.search_val = search_val
    self.result_db1 = result_db1
    self.result_db2 = result_db2
    self.t_begin = t_begin
    self.t_finish = t_finish
    self.t_thread1 = t_thread1
    self.t_thread2 = t_thread2
    self.t_thread3 = t_thread3

