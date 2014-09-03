#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common
from twisted.web import xmlrpc, server
from cqueue import *


'''
 Recebe Registro de Agente
 Toda comunicação é conferida através da confirmação do agente
 Requisições de todos os agentes entram para uma queue
 Essa queue é processada e registrada vinculada ao endereço ip do agente (profile por servidor)
 
 Agent: É o endereço IP do agente remoto, para identificar de qual servidor veio a request.
 Domain: Para registrar de qual empresa veio a request, para agrupar todos os IPS pertinentes.
 p_pid: vai identificar qual é o processo, dentro do servidor em questão, a qual cada item se refere
 

'''

class XmlHandler(xmlrpc.XMLRPC):
    def xmlrpc_register(self,address,domain,code):
        agent = code
        agent_address = address
        agent_domain = domain
        return True
    
    def xmlrpc_ping(self):
        return 1
    
    def xmlrpc_general(self,rcv_agent,rcv_domain,rcv_p_pid,rcv_p_name,rcv_p_uid,rcv_p_gid,rcv_p_rpm,rcv_p_dpkg,rcv_pf_path,rcv_pf_dac,rcv_pf_uid,rcv_pf_gid,rcv_p_args,rcv_p_tbanner,rcv_p_ubanner):
        print "[+] Registrando Dados Gerais"

        ParamDict={}
        ParamDict["agent"]=rcv_agent
        ParamDict["gateway"]=rcv_domain
        ParamDict["p_pid"]=rcv_p_pid
        ParamDict["p_name"]=rcv_p_name
        ParamDict["p_uid"]=rcv_p_uid
        ParamDict["p_gid"]=rcv_p_gid
        ParamDict["p_args"]=rcv_p_args
        ParamDict["p_rpm"]=rcv_p_rpm
        ParamDict["p_dpkg"]=rcv_p_dpkg
        ParamDict["pf_path"]=rcv_pf_path
        ParamDict["pf_dac"]=rcv_pf_dac
        ParamDict["pf_uid"]=rcv_pf_uid
        ParamDict["pf_gid"]=rcv_pf_gid
        ParamDict["tbanner"]=rcv_p_tbanner
        ParamDict["ubanner"]=rcv_p_ubanner
        print ParamDict["p_pid"]

        return True
    
    def xmlrpc_Fault(self):
        raise xmlrpc.Fault(123, "Erro.")











