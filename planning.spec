INIT_DATE 2/1/19

TASK Cil4sys sim
    COLOR #59a4af

    SUBTASK Familiarisation
        START_DATE 0w
        END_DATE 4w
    SUBTASK Intégration DQN 1/2
        START_DATE 4w
        END_DATE 8w
    SUBTASK Intégration DQN 2/2
        START_DATE 12w
        END_DATE 16w


TASK Flow DQN dev
    COLOR #59af92

    SUBTASK Small mesh DQN
        START_DATE 0w
        END_DATE 4w
    SUBTASK Model optimisation
        START_DATE 3w
        END_DATE 7w
    SUBTASK Large mesh DQN
        START_DATE 5w
        END_DATE 9w
    SUBTASK Model optimisation
        START_DATE 8w
        END_DATE 12w
    SUBTASK Final DQN
        START_DATE 11w
        END_DATE 14w
    SUBTASK Model optimisation
        START_DATE 12w
        END_DATE 16w
    SUBTASK Training
        START_DATE 16w
        END_DATE 18w

TASK Soutenance P3
    COLOR #926cad
    START_DATE 7w
    END_DATE 10w

TASK Soutenance P4
    COLOR #59A4AF
    START_DATE 18w
    END_DATE 21w
