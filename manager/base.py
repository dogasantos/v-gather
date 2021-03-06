#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# A organização dos casos funciona no esquema
# 2.5.1.1 Memória linear com busca serial (dumbo)
#
# A adaptação da solução será baseada em crítica.
# O usuário vai observar a solução e fazer a adaptação manualmente, caso seja necessário.
# Caso não seja necessário, a adaptação nula é adotada (apenas aplica como está)
#
#
#
#
import MySQLdb
from common import *
from cqueue import *

def DbConnect():
	try:
		ret=MySQLdb.connect(host=sqlhost, port=3306, user=sqluser, passwd=sqlpass, db=sqldb)
	except:
		ret=None
	return ret

def DbCountCases():
	conn=DbConnect()
	if conn == None:
		return False
	cursor = conn.cursor()
	case_sum="SELECT COUNT(id) from use_cases WHERE status=1"
	cursor.execute (case_sum)
	result = cursor.fetchone()
	conn.close()
	return int(result[0])

def DbGetCaseID():
	i=0
	total_cases=DbCountCases()
	if total_cases == False:
		print "  + Não existem casos na base. Cadastre-os primeiramente."
		return False
	query="SELECT id from use_cases WHERE status=1"
	conn=DbConnect()
	if conn == None:
			return False
	cursor = conn.cursor()
	cursor.execute (query)
	data = cursor.fetchall()
	conn.close()

	return data


def DbSimilarPoint():
	conn=DbConnect()
	if conn == None:
		return False
	cursor = conn.cursor()
	decpoint="SELECT value FROM case_match"
	cursor.execute (decpoint)
	result = cursor.fetchone()
	conn.close()
	return int(result[0])


def DbCheckAgent(agent_addr):
	conn=DbConnect()
	if conn == None:
		return False
	cursor = conn.cursor()
	ipaddr="SELECT id from managed_servers WHERE ipaddress like '%s'" %agent_addr
	cursor.execute (ipaddr)
	result = cursor.fetchone()
	conn.close()
	try:
		if int(result[0]) >0:
			return True
	except:
		return False

def DbGetCase(case_id):
	conn=DbConnect()
	if conn == None:
		return False
	if DbCountCases() == 0:
		# nao existem casos na base
		return 0 
	cursor = conn.cursor()
	query="SELECT id,\
	so_id, so_id_weight, \
	so_version, so_version_weight,\
	process_name, process_name_weight,\
	process_uid, process_uid_weight,\
	process_gid, process_gid_weight,\
	process_args, process_args_weight,\
	process_tcp_banner, process_tcp_banner_weight,\
	process_udp_banner, process_udp_banner_weight,\
	package_name, package_name_weight,\
	process_binary, process_binary_weight \
	from use_cases where id=%i and status=1" %case_id

	cursor.execute(query)
	results = cursor.fetchall()
	db_case={}
	db_case['case_id']=results[0][0]
	db_case['so_id']=results[0][1]
	db_case['so_id_weight']=results[0][2]
	db_case['so_version']=results[0][3]
	db_case['so_version_weight']=results[0][4]
	db_case['process_name']=results[0][5]
	db_case['process_name_weight']=results[0][6]
	db_case['process_uid']=results[0][7]
	db_case['process_uid_weight']=results[0][8]
	db_case['process_gid']=results[0][9]
	db_case['process_gid_weight']=results[0][10]
	db_case['process_args']=results[0][11]
	db_case['process_args_weight']=results[0][12]
	db_case['process_tcp_banner']=results[0][13]
	db_case['process_tcp_banner_weight']=results[0][14]
	db_case['process_udp_banner']=results[0][15]
	db_case['process_udp_banner_weight']=results[0][16]
	db_case['package_name']=results[0][17]
	db_case['package_name_weight']=results[0][18]
	db_case['process_binary']=results[0][19]
	db_case['process_binary_weight']=results[0][20]
	
	conn.close()
	return db_case

def DbGetSoName(so_id):
	conn=DbConnect()
	if conn == None:
		return False
	if DbCountCases == 0:
		# nao existem casos na base
		return 0 
	cursor = conn.cursor()
	query="SELECT name FROM sos WHERE id=%i" %int(so_id)
	cursor.execute(query)
	results = cursor.fetchone()
	conn.close()
	return results[0]
#
# Eu havia criado uma classe de fila
# pra instanciar filas como objetos.
# O problema é que quando eu alimentava os valores da 
# fila filtrada (a ser inserida na base),
# os valores float nos scores eram totalmente modificados.
# valor que deveria ser 3.0, estava como 0.45.
# nao consegui resolver esse problema, nao encontrei a causa raíz.
# fiquei um dia inteiro em cima desse problema e nada.
# pra evitar perder tanto tempo, mudei a abordagem
# ao invés de usar uma queue de dados pra inserir na base
# mandei inserir diretamente, sem queue.
# vai diminuir a performance, mas ...
def DbSimCases():
	clen=candidates.LenQueue()
	while clen > 0:
		pdict2={}
		pdict2=candidates.GetQueue()
		if pdict2['distro'].lower() == "debian":
			so_id=1
		else: 
			so_id=2
		print "*"*50
		for k,v in pdict2.items():
			if v == "" or len(str(v)) == 0:
				pdict2[k]="N/A"

			print "%s => %s" %(k,v)
		print "*"*50

		#
		# Dumbo - 5.5.4 Aprendizado - página 107
		# Após o caso ser solucionado, ele é encerrado podendo ou não ser aprendido pelo sistema.
		# Um caso é aprendido quando ele representa uma experiência nova, uma experiência para a qual
		# o sistema não foi capaz de propor uma solução adequada — seja porque o sistema propôs uma solução
		# que precisou ser adaptada, seja porque não propôs a melhor solução para a situação. Nesses casos,
		# a experiência obtida com o processo deve ser retida no sistema através de um novo caso.
		#
		#continue
		conn=DbConnect()
		if conn == None:
			return False
		cursor = conn.cursor()
		query = "INSERT INTO use_cases ( status, origem, case_id_related, \
										so_id, so_id_weight, so_id_score, \
										so_version, so_version_weight, so_version_score, \
										process_name, process_name_weight, process_name_score, \
										process_uid, process_uid_weight, process_uid_score, \
										process_gid, process_gid_weight, process_gid_score, \
										process_args, process_args_weight, process_args_score, \
										process_tcp_banner, process_tcp_banner_weight, process_tcp_banner_score, \
										process_udp_banner, process_udp_banner_weight, process_udp_banner_score, \
										package_name, package_name_weight, package_name_score, \
										process_binary, process_binary_weight, process_binary_score, \
										candidate_final_score) VALUES ( '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )" % ( 2, 2, str(pdict2['case_id_related']),str(so_id), str(pdict2['distro_weight']), str(pdict2['distro_score']), str(pdict2['distro_version']), str(pdict2['distro_version_weight']), str(pdict2['distro_version_score']), str(pdict2['p_name']),str(pdict2['p_name_weight']), str(pdict2['p_name_score']), str(pdict2['p_uid']), str(pdict2['p_uid_weight']), str(pdict2['p_uid_score']), str(pdict2['p_gid']), str(pdict2['p_gid_weight']), str(pdict2['p_gid_score']), str(pdict2['p_args']),str(pdict2['p_args_weight']), str(pdict2['p_args_score']), str(pdict2['p_tcp_banner']), str(pdict2['p_tcp_banner_weight']), str(pdict2['p_tcp_banner_score']), str(pdict2['p_udp_banner']), str(pdict2['p_udp_banner_weight']), str(pdict2['p_udp_banner_score']), str(pdict2['p_package']), str(pdict2['p_pkg_weight']), str(pdict2['p_pkg_score']), str(pdict2['pf_path']), str(pdict2['pf_path_weight']), str(pdict2['pf_path_score']), str(round(pdict2['score'],2)) )
		
		cursor.execute(query)
		conn.commit()
		conn.close ()
		clen-=1

	candidates.DestroyQueue()





