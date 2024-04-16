
from getpass import getpass 
from prompt_toolkit import PromptSession 
session = PromptSession() 


class Views(): 
    print('hello view') 

    # def input_user_email(self): 
    #     """ Prompts to the user's email, in order to check if he/she has a token. 
    #         Returns: 
    #             str: The user's email. 
    #     """ 
    #     email = session.prompt('\nAdresse mail : ') 
    #     return email 

    def input_user_connection(self): 
        """ Prompt to the data to connect a user. 
            Returns:
                dict: The data for connecting the user. 
        """ 
        user = {} 
        user['email'] = session.prompt('\nAdresse mail : ') 
        user['password'] = getpass('\nMot de passe : ') 
        return user 


# ==== displaying non generics ==== # 
    def display_user_minimum(self, user): 
        print(f'\nUtilisateur : \nid : :{user.id}, {user.name}, département : {user.department.name} (ID : {user.department_id})') 
# ==== /displaying non generics ==== # 


# ==== generics ==== # 
    def input_select_entity(self, entity): 
        """ Select an entity, in order to do other action with the object's data, 
            or just for displaying it. 
            Args: 
                entity (str): The name of the entity. 
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
        entity_dict = {} 
        entity_dict['chosen_field'] = session.prompt(f'\nSur quel champ voulez-vous sélectionner {entity_str[entity]} ? ') 
        entity_dict['value_to_select'] = session.prompt('\nValeur à sélectionner : ') 
        return entity_dict 


    def display_entity(self, objects:list): 
        """ Displays one or many entity/ies from a given table, 
            using the str() of each model. 
            Args: 
                objects (list): The objects to display. 
        """ 
        for obj in objects: 
            print(obj) 


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

    def ask_for_creation(self, entity): 
        """ Prompt to confirm the creation of the item with the given data. 
            Possible entities: 
                'dept', 'user', 'client', 'contract', 'event'. 
            Args: 
                entity (str): The entity to delete or modify. 
            Returns:
                str: The answer from the user. 
        """ 
        entity_name = { 
            'dept': 'nouveau département', 
            'user': 'nouvel utilisateur',
            'client': 'nouveau client', 
            'contract': 'nouveau contrat', 
            'event': 'nouvel événement'
        } 
        print(f'\nVous êtes sur le point d\'enregistrer un {entity_name[entity]} avec les informations suivantes : ') 
        print(entity) 
        return confirmation 
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
        # user['department_id'] = session.prompt('\nDépartement (auto) : ') 
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
        # client['sales_contact_name'] = auto 
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
        event['contract_id'] = session.prompt('\nID du contrat (numéro) : ') 
        event['start_datetime'] = session.prompt('\nDate / heure de début (format) : ') 
        event['end_datetime'] = session.prompt('\nDate / heure de fin (format) : ') 
        # event['support_contact_name'] = (auto) 
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
        print(f'Modifier le département : ') 
        self.display_entity([old_dept]) 
        dept = old_dept.to_dict() 
        dept['new_name'] = session.prompt('\nNouveau nom du département : ') 
        return dept 


    def input_modify_entity(self, entity, old_entity, gestion=False): 
        """ Prompt the data to modify an entity into the DB. 
            Args: 
                entity (str): The name of the table of the entity to modify. 
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
        print('input_modify_entity (views)') 
        print('old_entity : ', old_entity)  # ok 
        # print('entity : ', entity) 
        # print('gestion : ', gestion) 
        print(f'Modifier {entity_str[entity]} : ') 

        # problème : 
        self.display_entity([old_entity]) 
        entity_dict = old_entity.to_dict() 
        if (entity == 'event') & gestion: 
            entity_dict['field_to_modify'] = 'support_contact_id' 
            entity_dict['new_value'] = session.prompt(f"\nNouvelle valeur pour le champ ''support_contact_id'' (ID) : ") 
            return entity_dict 
        else: 
            entity_dict['field_to_modify'] = session.prompt('\nQuel champ voulez-vous modifier ? ') 
            entity_dict['new_value'] = session.prompt(f"\nNouvelle valeur pour le champ {entity_dict['field_to_modify']} : ") 
            print('entity_dict (views) : ', entity_dict) 
            return entity_dict 


    def input_modify_user(self, old_user): 
        """ Prompt the data to modify a user into the DB. 
            Args: 
                old_user (object): The registered entity to modify. 
            Returns: 
                dict: The new data to register into the DB. 
        """ 
        print(f'Modifier l\'utilisateur : ') 
        self.display_entity([old_user]) 
        user = old_user.to_dict() 
        user['field_to_modify'] = session.prompt('\nQuel champ voulez-vous modifier ? ') 
        user['new_value'] = session.prompt(f"\nNouvelle valeur pour le champ {user['field_to_modify']} : ") 
        print('user (views) : ', user) 
        return user 


    def input_modify_client(self, old_client): 
        print('Modifier le client : ') 
        self.display_entity([old_client]) 
        #     ID : {old_event.id} 
        #     nom : {old_event.name} 
        #     ID contrat : {old_event.contract_id} 
        #     client : {old_event.contracts.client.name} (id : {old_event.contracts.client.name}) 
        #     début : {old_event.start_datetime} 
        #     fin : {old_event.end_datetime} 
        #     contact support : {old_event.user.name} (id : {old_event.support_contact_id})') 
        #     lieu : {old_event.location} 
        #     invités : {old_event.attendees} 
        #     notes : {old_event.notes} 
        # ''') 
        client = old_client.to_dict() 
        client['field_to_modify'] = session.prompt('\nQuel champ voulez-vous modifier ? ') 
        client['new_value'] = session.prompt(f"\nNouvelle valeur pour le champ {client['field_to_modify']} : ") 
        print('client (views) : ', client) 
        return client 


    def input_modify_contract(self, old_contract): 
        print('Modifier le contrat : ') 
        self.display_entity([old_contract]) 
        contract = old_contract.to_dict() 
        contract['field_to_modify'] = session.prompt('\nQuel champ voulez-vous modifier ? ') 
        contract['new_value'] = session.prompt(f"\nNouvelle valeur pour le champ {contract['field_to_modify']} : ") 
        print('contrat (views) : ', contract) 
        return contract 

