import os
import logging
import logging.config

from paiLibrary.paiService import service_management_start
from paiLibrary.paiService import service_management_stop
from paiLibrary.paiService import service_management_delete
from paiLibrary.paiService import service_management_refresh

logger = logging.getLogger(__name__)


class ServiceCmd():
    def register(self, parser):
        service_parser = parser.add_subparsers(help="service operations")

        # ./paictl.py service start ...
        start_parser = service_parser.add_parser("start")
        start_parser.set_defaults(handler=self.service_start)

        # ./paictl.py service stop ...
        stop_parser = service_parser.add_parser("stop")
        stop_parser.set_defaults(handler=self.service_stop)

        # ./paictl.py service delete ...
        delete_parser = service_parser.add_parser("delete")
        delete_parser.set_defaults(handler=self.service_delete)

        # ./paictl.py service refresh
        refresh_parser = service_parser.add_parser("refresh")
        refresh_parser.set_defaults(handler=self.service_refresh)

        def add_arguments(parser):
            parser.add_argument("-c", "--kube-config-path", dest="kube_config_path", default="~/.kube/config", help="The path to KUBE_CONFIG file. Default value: ~/.kube/config")
            parser.add_argument("-n", "--service-name", dest="service_name", default="all", help="Build and push the target image to the registry")

        add_arguments(start_parser)
        add_arguments(stop_parser)
        add_arguments(delete_parser)
        add_arguments(refresh_parser)

    def process_args(self, args):
        if args.kube_config_path != None:
            args.kube_config_path = os.path.expanduser(args.kube_config_path)

        service_list = None
        if args.service_name != "all":
            service_list = [args.service_name]

        return service_list

    def service_start(self, args):
        service_list = self.process_args(args)

        service_management_starter = service_management_start.serivce_management_start(args.kube_config_path, service_list)
        service_management_starter.run()

    def service_stop(self, args):
        service_list = self.process_args(args)

        service_management_stopper = service_management_stop.service_management_stop(args.kube_config_path, service_list)
        service_management_stopper.run()

    def service_delete(self, args):
        service_list = self.process_args(args)

        logger.warning("--------------------------------------------------------")
        logger.warning("--------------------------------------------------------")
        logger.warning("----------     Dangerous Operation!!!    ---------------")
        logger.warning("------     The target service will be stopped    -------")
        logger.warning("------    And the persistent data on the disk    -------")
        logger.warning("-------             will be deleted             --------")
        logger.warning("--------------------------------------------------------")
        logger.warning("--------------------------------------------------------")
        logger.warning("--------     It's an irreversible operation      -------")
        logger.warning("--------           After this operation,         -------")
        logger.warning("------ the deleted service data is unrecoverable -------")
        logger.warning("--------------------------------------------------------")
        logger.warning("--------------------------------------------------------")
        logger.warning("----    Please ensure you wanna do this operator, ------")
        logger.warning("-------        after knowing all risk above.     -------")
        logger.warning("--------------------------------------------------------")
        logger.warning("--------------------------------------------------------")

        count_input = 0
        while True:
            user_input = raw_input("Do you want to continue this operation? (Y/N) ")
            if user_input == "N":
                return
            elif user_input == "Y":
                break
            else:
                print(" Please type Y or N.")
            count_input = count_input + 1
            if count_input == 3:
                logger.warning("3 Times.........  Sorry,  we will force stopping your operation.")
                return

        service_management_deleter = service_management_delete.service_management_delete(args.kube_config_path, service_list)
        service_management_deleter.run()

    def service_refresh(self, args):
        service_list = self.process_args(args)

        service_management_refresher = service_management_refresh.service_management_refresh(args.kube_config_path, service_list)
        service_management_refresher.run()
