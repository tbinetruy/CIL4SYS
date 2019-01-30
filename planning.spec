INIT_DATE 2/1/19

TASK Cil4sys sim
    COLOR #59a4af

    SUBTASK (AM) Familiarisation
        START_DATE 0w
        END_DATE 4w
    SUBTASK (TP) Intégration DQN 1/2
        START_DATE 4w
        END_DATE 8w
    SUBTASK (TP) Intégration DQN 2/2
        START_DATE 12w
        END_DATE 16w


TASK Flow DQN dev
    COLOR #59af92

    SUBTASK (TP) Small mesh DQN
        START_DATE 0w
        END_DATE 4w
    SUBTASK (AM) Model optimisation
        START_DATE 3w
        END_DATE 7w
    SUBTASK (TP) Large mesh DQN
        START_DATE 5w
        END_DATE 9w
    SUBTASK (AM) Model optimisation
        START_DATE 8w
        END_DATE 12w
    SUBTASK (TP) Final DQN
        START_DATE 11w
        END_DATE 14w
    SUBTASK (AM) Model optimisation
        START_DATE 12w
        END_DATE 16w
    SUBTASK (TPAM) Training
        START_DATE 16w
        END_DATE 18w

TASK (TPAM) Restitution
    COLOR #6b71b4
    START_DATE 18w
    END_DATE 20w
