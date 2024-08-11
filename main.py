(lambda: (memory := {
        'main': lambda mem: mem['while'](lambda: not mem['is_game_over'][0], lambda a, b: mem['update'](mem)),
        'while': lambda condition, code: __import__('functools').reduce(code, iter(condition, False)),
        'WIDTH': 100,
        'HEIGHT': 50,
        'PADDLE_HEIGHT': 20,
        'SLOW_DOWN': 8,
        'ACCEL': 20,
        'MAX_SPEED': 15,
        'BALL_SPEED_FACTOR': 1.1,
        'TARGET_DELTA_TIME': 0.15,
        'INPUTS': {'p1': [0], 'p2': [0]},
        'p1': {'pos': [0], 'vel': [0]},
        'p2': {'pos': [0], 'vel': [0]},
        'ball': {'pos': [50, 25], 'vel': [10, 0]},
        'is_game_over': [False],
        'delta_time': [0],
        'start': [__import__('time').time()],
        'update': lambda mem: (time := __import__('time').time(),
                               delta_time := time - (mem['start'][0]),
                               mem['delta_time'].clear(),
                               mem['delta_time'].append(delta_time),
                               mem['update_input'](mem),
                               (mem['update_ball'](mem),
                                mem['update_player']('p1', mem),
                                mem['update_player']('p2', mem),
                                mem['detect_impact'](mem),
                                mem['clear'](),
                                mem['draw'](mem),
                                print(f"p1: {mem['p1']}"),
                                print(f"p2: {mem['p2']}"),
                                print(f"ball: {mem['ball']}"),
                                mem['start'].clear(),
                                mem['start'].append(time)
                                ) if delta_time >= mem['TARGET_DELTA_TIME'] else None,
                               ),
        'draw': lambda mem: (
                p1_pos := mem['p1']['pos'][0],
                p2_pos := mem['p2']['pos'][0],
                ball_pos := mem['ball']['pos'],
                print("".join(["\n" + "".join(["#" if ((y >= p1_pos) and (y <= (p1_pos + mem['PADDLE_HEIGHT'])) and (x == 0)) or
                                                        ((y >= p2_pos) and (y <= (p2_pos + mem['PADDLE_HEIGHT'])) and (x == mem['WIDTH'] - 1))
                                                else '@' if (int(ball_pos[0]) == x) and (int(ball_pos[1]) == y) else " "
                                               for x in range(mem['WIDTH'])]) for y in range(mem['HEIGHT'])]))
        ),
        'clear': lambda: __import__('os').system("cls"),
        'update_input': lambda mem: (
                inputs := mem['INPUTS'],
                inputs['p1'].clear(),
                inputs['p2'].clear(),
                inputs['p1'].append((int(__import__('keyboard').is_pressed('s') - int(__import__('keyboard').is_pressed('w'))))),
                inputs['p2'].append((int(__import__('keyboard').is_pressed('down') - int(__import__('keyboard').is_pressed('up')))))
        ),
        'end_game': lambda mem: (mem['is_game_over'].clear(),
                                 mem['is_game_over'].append(True)),
        'update_player': lambda player_name, mem: (
                player := mem[player_name],
                pos := player['pos'][0],
                speed := player['vel'][0],
                slowed := speed - (__import__('math').copysign(mem['SLOW_DOWN'], speed) * mem['delta_time'][0]),
                speed := slowed if (__import__('math').copysign(slowed, speed) == slowed) else 0,
                speed := speed + ((mem['INPUTS'][player_name][0] * (mem['delta_time'][0]) * mem['ACCEL'])/2),
                pos := min(max(pos + (speed*(mem['delta_time'][0])), 0), mem['HEIGHT'] - mem['PADDLE_HEIGHT']),
                speed := speed + ((mem['INPUTS'][player_name][0] * (mem['delta_time'][0]) * mem['ACCEL'])/2),
                speed := min(max(speed, -mem['MAX_SPEED']), mem['MAX_SPEED']),
                player['pos'].clear(),
                player['pos'].append(pos),
                player['vel'].clear(),
                player['vel'].append(speed)
                ),
        'update_ball': lambda mem: (
                ball_pos := mem['ball']['pos'],
                ball_vel := mem['ball']['vel'],
                delta := [v * mem['delta_time'][0] for v in ball_vel],
                ball_pos := [ball_pos[i] + delta[i] for i in range(len(ball_pos))],
                mem['ball']['pos'].clear(),
                [mem['ball']['pos'].append(p) for p in ball_pos],
                ball_vel := [(-ball_vel[i]) * (mem['BALL_SPEED_FACTOR']) if i == 0 and ((ball_pos[0] <= 0) or (ball_pos[0] >= mem['WIDTH'] - 1))
                             else ball_vel[i] + mem['p1']['vel'][0] if (ball_pos[0] <= 0)
                                else ball_vel[i] + mem['p2']['vel'][0] if (ball_pos[0] >= mem['WIDTH'] - 1)
                                else ball_vel[i] for i in range(len(ball_vel))],
                ball_vel := [-ball_vel[i] if (i == 1) and ((ball_pos[1] <= 0) or (ball_pos[1] >= mem['HEIGHT'] - 1)) else ball_vel[i] for i in range(len(ball_vel))],
                mem['ball']['vel'].clear(),
                [mem['ball']['vel'].append(p) for p in ball_vel]
        ),
        'detect_impact': lambda mem: (
            ball_pos := mem['ball']['pos'],
            mem['end_game'](mem) if ((ball_pos[0] <= 0) and not ((mem['p1']['pos'][0] <= ball_pos[1]) and
                     (mem['p1']['pos'][0] + mem['PADDLE_HEIGHT'] >= ball_pos[1]))) or
                    ((ball_pos[0] >= mem['WIDTH'] - 1) and not ((mem['p2']['pos'][0] <= ball_pos[1]) and
                    (mem['p2']['pos'][0] + mem['PADDLE_HEIGHT'] >= ball_pos[1])))
            else None
        )
        }, memory['main'](memory)))()
# memory contains everything in the program (every variable and every function)
# every function is written as a lambda
# every function that needs something from memory needs to get memory as a parameter
# memory['main'] is the main function
# a value is constant and cant be reassigned if its not in a list, if a value should change it should be written [value]
# when using a while the code parameter should always get 2 parameters