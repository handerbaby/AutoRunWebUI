from common.factory import Factory

factory = Factory()
isOk, result = factory.init_excute_case()
for cases_list in result:
    for key, cases in cases_list.items():
        for case in cases:
            isOk, result = factory.execute_keyword(**case)
            print(result)
