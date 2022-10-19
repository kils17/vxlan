# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service



def get_peer_tenant(service, my_tenant):
  
  peers = []

  for tenant in service.tenant:
    if tenant.name != my_tenant:
      peers.append(tenant.name)
    
  return peers
       

# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')


        for tenant in service.tenant:
          self.log.info('tenant : ', tenant.name)

          my_tenant = root.vxlanTenant[tenant.name]
          self.log.info('my tenant : ', my_tenant.name)


          self.log.info(' - vtep : ', my_tenant.vtep)
          for vtep in my_tenant.vtep:

            peer_tenants = get_peer_tenant(service, tenant.name)
 
            for peer in peer_tenants:
              peer_tenant = root.vxlanTenant[peer]

              self.log.info('   - device : ', vtep.switch)
              self.log.info('   - tenant : ', my_tenant.name)
              self.log.info('   - asn : ', my_tenant.asn)
              self.log.info('   - peer_vni : ', str(peer_tenant.vnid_prefix) + str(peer_tenant.l3_vlanid))
            
              vars = ncs.template.Variables()
              vars.add('device', vtep.switch)
              vars.add('tenant', my_tenant.name)
              vars.add('asn', my_tenant.asn)
              vars.add('peer_vni', str(peer_tenant.vnid_prefix) + str(peer_tenant.l3_vlanid))

              template = ncs.template.Template(service)
              template.apply('vxlanVrfleaking-template', vars)

    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service postmod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('vxlanVrfleaking-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
