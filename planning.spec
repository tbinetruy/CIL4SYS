INIT_DATE 20/1/19

TASK Flow DQN dev
    COLOR #59AF92
    SUBTASK Small mesh DQN
        START_DATE 0w
        END_DATE 4w
    SUBTASK Model optimisation
        START_DATE 4w
        END_DATE 8w
    SUBTASK Large mesh DQN
        START_DATE 6w
        END_DATE 10w
    SUBTASK Model optimisation
        START_DATE 12w
        END_DATE 16w

TASK CIL4SYS sim
    COLOR #59A4AF

    SUBTASK Getting started
        START_DATE 0w
        END_DATE 2w
    SUBTASK Dqn integration
        START_DATE 0w
        END_DATE 8w

TASK Delivery
    COLOR #6b71b4

    SUBTASK Training
        START_DATE 16w
        END_DATE 18w
    SUBTASK Restitution
        START_DATE 18w
        END_DATE 20w
