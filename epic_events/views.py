
from getpass import getpass 
from prompt_toolkit import PromptSession 
session = PromptSession() 


class Views(): 
    print('hello view') 


# ==== non generics ==== # 
    def input_user_connection_email(self): 
        """ Prompt to the email to connect a user. 
            Returns:
                dict: The email for connecting the user. 
        """ 
        userEmail = session.prompt('\nAdresse mail : ') 
        return userEmail 

    def input_user_connection_pass(self): 
        """ Prompt to the password to connect a user. 
            Returns:
                dict: The password for connecting the user. 
        """ 
        userPass = getpass('\nMot de passe : ') 
        return userPass 


    def display_user_minimum(self, user): 
        print(f'\nUtilisateur : \nid :{user.id}, {user.name}, département : {user.department.name} (ID : {user.department_id})') 
# ==== /non generics ==== # 


# ==== generics ==== # 
    def input_select_entity(self, entity_name): 
        """ Select an entity, in order to do other action with the object's data, 
            or just for displaying it. 
            Args: 
                entity_name (str): The name of the entity. 
                Possible names: 
                    'dept' 
                    'user' 
                    'client' 
                    'contract' 
                    'event'. 
            Returns: 
                object: The selected object instance. 
        """ 
        entity_str = { 
            'dept': 'le département', 
            'user': 'l\'utilisateur', 
            'client': 'le client', 
            'contract': 'le contrat', 
            'event': 'l\'événement', 
        } 
        if entity_name == 'dept': 
            fields = ['id', 'name'] 
        elif entity_name == 'user': 
            fields = ['id', 'name', 'email'] 
        elif entity_name == 'client': 
            fields = ['id', 'name', 'email', 'phone'] 
        elif entity_name == 'contract': 
            fields = ['id'] 
        elif entity_name == 'event': 
            fields = ['id', 'name', 'contract_id'] 
        print('Les champs possibles sont: ') 
        for f in fields: 
            print(f) 
        entity_dict = {} 
        entity_dict['field_to_select'] = session.prompt(f'\nSur quel champ voulez-vous sélectionner {entity_str[entity_name]} ? ') 
        entity_dict['value_to_select'] = session.prompt('\nValeur à sélectionner : ') 
        return entity_dict 

    
    def input_modify_entity(self, entity_name, old_entity, gestion=False): 
        """ Prompt the data to modify an entity into the DB. Not for departments. 
            Args: 
                entity_name (str): The name of the table of the entity to modify. 
                old_entity (object): The registered entity to modify. 
            Returns: 
                dict: The new data to register into the DB. 
        """ 
        entity_str = { 
            'user': 'l\'utilisateur', 
            'client': 'le client', 
            'contract': 'le contrat', 
            'event': 'l\'événement', 
        } 
        print('\ninput_modify_entity (views)') 
        print(f'\nModifier {entity_str[entity_name]} : ') 

        self.display_entity([old_entity]) 
        entity_dict = old_entity.to_dict() 
        if (entity_name == 'event') & gestion: 
            entity_dict['field_to_modify'] = 'support_contact_name' 
            entity_dict['new_value'] = session.prompt(f"\nNouvelle valeur pour le champ ''support_contact_name'' (name) : ") 
            return entity_dict 
        else: 
            entity_dict['field_to_modify'] = session.prompt('\nQuel champ voulez-vous modifier ? ') 
            entity_dict['new_value'] = session.prompt(f"\nNouvelle valeur pour le champ {entity_dict['field_to_modify']} : ") 
            return entity_dict 


    def display_entity(self, objects:list): 
        """ Displays one or many entity/ies from a given table, 
            using the str() of each model. 
            Args: 
                objects (list): The objects to display. 
        """ 
        print(objects) 
        for obj in objects: 
            print(obj) 

    def display_dict(self, entity_name, dict_to_register): 
        """ Displays the input data to register. 
            Args: 
                dict: The dictionary of data to register. 
        """ 
        if entity_name == 'user': 
            print(f"nom : {dict_to_register['name']}, mail: {dict_to_register['email']}, mot de passe: (secret), téléphone: {dict_to_register['phone']}, nom du département : {dict_to_register['department_name']}") 
        else: 
            print(dict_to_register) 


    def ask_for_confirmation(self, action, entity): 
        """ Prompt to confirm the modification or deletion of an item from the DB. 
            Possible actions: 
                supprimer, modifier. 
            Possible entities: 
                'dept', 'user', 'client', 'contract', 'event'. 
            Args:
                action (str): The verb of the action to perform. 
                entity (str): The entity to delete or modify. 
            Returns:
                str: The answer from the user. 
        """ 
        entity_dict = { 
            'dept': 'ce département', 
            'user': 'cet utilisateur',
            'client': 'ce client', 
            'contract': 'ce contrat', 
            'event': 'cet événement' 
        } 
        confirmation = session.prompt(f'\nEtes-vous sûr de vouloir {action} {entity_dict[entity]} ? (Y/N) ') 
        return confirmation 

    def enter_to_continue(self): 
        enter = session.prompt('Appuyez sur entrée pour continuer ') 
        return enter 

    # ==== generics ==== # 


    # ==== creations ==== # 
    def input_create_dept(self): 
        """ Prompt the department name to select it into the DB. 
            Returns:
                dict: The name of the department, on which to select it. 
        """  
        dept = {} 
        dept['name'] = session.prompt('\nNom du département : ') 
        return dept 

    def input_user_role(self): 
        """ Prompt the role of the new pre-registered user (only when mode == 'dev'). 
            Returns:
                str: The role in 'sales' and 'support'. 
        """ 
        user_role = session.prompt('\nRôle de l\'utilisateur : ') 
        return user_role 

    def input_create_user(self): 
        """ Prompt the data to register a new user. 
            Returns:
                dict: The data to register into the DB. 
        """ 
        user = {} 
        user['name'] = session.prompt('\nNom de l\'utilisateur : ') 
        user['email'] = session.prompt('\nMail : ') 
        user['entered_password'] = getpass('\nMot de passe : ') 
        user['phone'] = session.prompt('\nTéléphone : ') 
        user['department_name'] = session.prompt('\nNom du département : ') 
        return user 

    def input_create_client(self): 
        """ Prompt the data to register a new client. 
            Returns:
                dict: The data to register into the DB. 
        """ 
        client = {} 
        client['name'] = session.prompt('\nNom du client : ') 
        client['email'] = session.prompt('\nMail : ') 
        client['phone'] = session.prompt('\nTéléphone : ') 
        client['corporation_name'] = session.prompt('\nNom de l\'entreprise : ') 
        return client 

    def input_create_contract(self): 
        """ Prompt the data to register a new contract. 
            Returns:
                dict: The data to register into the DB. 
        """ 
        contract = {} 
        contract['client_name'] = session.prompt('\nNom du client : ') 
        contract['is_signed'] = session.prompt('Contrat signé ? (Y/N) : ') 
        contract['amount'] = session.prompt('Montant dû : ') 
        contract['paid_amount'] = session.prompt('Quel montant réglé ? : ') 
        return contract 

    def input_create_event(self): 
        """ Prompt the data to register a new event. 
            Returns:
                dict: The data to register into the DB. 
        """ 
        event = {} 
        event['name'] = session.prompt('\nNom de l\'événement : ') 
        event['start_datetime'] = session.prompt('\nDate / heure de début (format) : ') 
        event['end_datetime'] = session.prompt('\nDate / heure de fin (format) : ') 
        event['location'] = session.prompt('\nLieu / adresse : ') 
        event['attendees'] = session.prompt('\nNombre de aprticipants : ') 
        event['notes'] = session.prompt('\nNotes : ') 
        return event 
    # ==== /creations ==== # 


    # ==== modifications ==== # 
    def input_modify_dept(self, old_dept): 
        """ Prompt the data to modify a department into the DB. 
            Args: 
                old_dept (str): The registered department to modify. 
            Returns: 
                dict: The new data to register into the DB. 
        """ 
        print(f'\nModifier le département : ') 
        self.display_entity([old_dept]) 
        dept = old_dept.to_dict() 
        dept['new_name'] = session.prompt('\nNouveau nom du département : ') 
        return dept 

