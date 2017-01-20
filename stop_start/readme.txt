stop:
./stop_start_services.py -a http://10.32.14.12:84 -u /root/root -p ~/npass --nodeuser nimbulaadmin --nodepass ~/npass --services storage_metadata,storage_writable,storage_secondary,storage_node,storage_master,gluster_mount,gluster_server  --put stop_start_node_service.py --type stop -n http://10.32.14.11:84

start:
./stop_start_services.py -a http://10.32.14.12:84 -u /root/root -p ~/npass --nodeuser nimbulaadmin --nodepass ~/npass --services storage_metadata,storage_writable,storage_secondary,storage_node,storage_master,gluster_mount,gluster_server --put stop_start_node_service.py --type start -n http://10.32.14.11:84


snapshot:
./sss -a http://10.32.30.12:84 -u /root/root -p ~/npass --nodeuser
nimbulaadmin --nodepass ~/npass --services
storage_metadata,storage_writable,storage_secondary,storage_node,storage_master,gluster_mount,gluster_server
 --type snapshot
