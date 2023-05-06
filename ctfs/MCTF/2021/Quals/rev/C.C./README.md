Backend SQL definition:

CREATE TABLE api_client
(
    created_at      timestamp WITH TIME ZONE NOT NULL,
    modified_at     timestamp WITH TIME ZONE NOT NULL,
    ip              inet                     NOT NULL
        CONSTRAINT api_client_pkey
            PRIMARY KEY,
    platform        varchar(1)               NOT NULL,
    os_version      varchar(128)             NOT NULL,
    killswitch_path text                     NOT NULL,
    last_ping_time  timestamp WITH TIME ZONE NOT NULL
);

CREATE TABLE api_scheduledaction
(
    id          bigserial
        CONSTRAINT api_scheduledaction_pkey
            PRIMARY KEY,
    created_at  timestamp WITH TIME ZONE NOT NULL,
    modified_at timestamp WITH TIME ZONE NOT NULL,
    action_type varchar(2)               NOT NULL,
    platform    varchar(1)               NOT NULL,
    payload     text                     NOT NULL
);

CREATE TABLE api_result
(
    id          bigserial
        CONSTRAINT api_result_pkey
            PRIMARY KEY,
    created_at  timestamp WITH TIME ZONE NOT NULL,
    modified_at timestamp WITH TIME ZONE NOT NULL,
    content     text                     NOT NULL,
    action_id   bigint
        CONSTRAINT api_result_action_id_07af5139_fk_api_scheduledaction_id
            REFERENCES api_scheduledaction
            DEFERRABLE INITIALLY DEFERRED,
    client_id   inet
        CONSTRAINT api_result_client_id_cd34f92b_fk_api_client_ip
            REFERENCES api_client
            DEFERRABLE INITIALLY DEFERRED
);

Models definition:

class Client(TimeDateMixin, ChangesNotificationMixin):
    class Platform(models.TextChoices):
        LINUX = 'L'
        WINDOWS = 'W'
        UNKNOWN = 'U'

    ip = models.GenericIPAddressField('IP Address', unpack_ipv4=True, primary_key=True)
    platform = models.CharField('OS', choices=Platform.choices, max_length=1)
    os_version = models.CharField('OS version', max_length=128, blank=True)
    killswitch_path = models.TextField('killswitch file path')
    last_ping_time = models.DateTimeField('last alive ping')

class ScheduledAction(TimeDateMixin, ChangesNotificationMixin):
    class Types(models.TextChoices):
        SHELL_CMD = 'SH'
        """Execute custom shell command."""
        SHELL_AUTO = 'SA'
        """Execute custom shell command on client first connection."""
        FLAG = 'FL'
        """Contains flag."""

    class ExecuteOnPlatform(models.TextChoices):
        LINUX = 'L'
        WINDOWS = 'W'
        BOTH = 'B'

    action_type = models.CharField('type', choices=Types.choices, max_length=2)
    platform = models.CharField('execute on os', choices=ExecuteOnPlatform.choices, max_length=1)
    execute_on = models.ManyToManyField(Client, related_name='scheduled_actions', verbose_name='scheduled on')

    payload = models.TextField('payload', blank=True)

class Result(TimeDateMixin, ChangesNotificationMixin):
    client = models.ForeignKey(Client, verbose_name='on client', related_name='results',
                               on_delete=models.SET_NULL, null=True, blank=True)
    action = models.ForeignKey(ScheduledAction, verbose_name='by action', related_name='results',
                               on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField('execution results', blank=True)
