
from getpass import getpass 
from prompt_toolkit import PromptSession 
session = PromptSession() 


class Views(): 
    print('hello view') 

    def input_user_connection(self): 
        user = {} 
        user['email'] = session.prompt('\nAdresse mail : ') 
        user['password'] = getpass('\nMot de passe : ') 
        # user['email'] = getpass('\nAdresse mail : ') 
        # user['password'] = session.prompt('\nMot de passe : ') 
        return user 


    def input_create_dept(self): 
        dept = {} 
        dept['name'] = session.prompt('\nNom du département : ') 
        return dept 


    def input_create_user(self): 
        user = {} 
        user['name'] = session.prompt('\nNom de l\'utilisateur : ') 
        user['email'] = session.prompt('\nMail : ') 
        # user['email'] = session.prompt('\nMail : ') 
        user['entered_password'] = getpass('\nMot de passe : ') 
        user['phone'] = session.prompt('\nTéléphone : ') 
        user['department_name'] = session.prompt('\nNom du département : ') 
        # user['department_id'] = session.prompt('\nDépartement (auto) : ') 
        return user 


    def input_create_client(self): 
        client = {} 
        client['name'] = session.prompt('\nNom du client : ') 
        client['email'] = session.prompt('\nMail : ') 
        client['phone'] = session.prompt('\nTéléphone : ') 
        client['corporation_name'] = session.prompt('\nNom de l\'entreprise : ') 
        # client['sales_contact_name'] = session.prompt('\nContact commercial (auto) : ') 
        return client 


    def input_create_contract(self): 
        contract = {} 
        contract['client_name'] = session.prompt('\nNom contact commercial : ') 
        contract['is_signed'] = session.prompt('\nContrat signé ? (Y/N) : ') 
        contract['amount'] = session.prompt('\nMontant dû : ') 
        contract['paid_amount'] = session.prompt('\nMontant réglé : ') 
        return contract 


    def input_create_event(self): 
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


    def input_select_entity(self, entity): 
        """ Select an entity (except Department), in order to do other action with the object's data, 
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
        if entity == 'dept': 
            entity_dict['old_value'] = session.prompt('\nNom du département à sélectionner : ') 
        else: 
            entity_dict['chosen_field'] = session.prompt(f'\nSur quel champ voulez-vous sélectionner {entity_str[entity]} ? ') 
            entity_dict['old_value'] = session.prompt('\nValeur à sélectionner : ') 
        return entity_dict 


    def input_modify_dept(self, old_dept): 
        print(f'Modifier le département : ') 
        self.display_entity([old_dept]) 
        dept = old_dept.to_dict() 
        dept['new_name'] = session.prompt('\nNouveau nom du département : ') 
        return dept 


    def input_modify_user(self, old_user):  # , field_to_modify): 
        print(f'Modifier l\'utilisateur : ') 
        self.display_entity([old_user]) 
        #     id : {old_user.id} 
        #     name : {old_user.name} 
        #     email : {old_user.email} 
        #     password : {old_user.password} 
        #     téléphone : {old_user.phone} 
        #     département : {old_user.department.name} (id : {old_user.department_id}) 
        # ''') 
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


    def input_modify_event(self, old_event, gestion=False):  # , field_to_modify): 
        print('Modifier l\'événement : ') 
        self.display_entity([old_event]) 
        # print(f'''
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
        event = old_event.to_dict() 
        if not gestion: 
            event['field_to_modify'] = session.prompt('\nQuel champ voulez-vous modifier ? ') 
            event['new_value'] = session.prompt(f"\nNouvelle valeur pour le champ {event['field_to_modify']} : ") 
        else: 
            event['field_to_modify'] = 'support_contact_id' 
            event['new_value'] = session.prompt(f"\nNouvelle valeur pour le champ ''support_contact_id'' (ID) : ") 
        print('event (views) : ', event) 
        return event 


    def display_entity(self, objects:list): 
        for obj in objects: 
            print(obj) 
            # print(f''' 
            #     id : {obj.id} 
            #     name : {obj.name} 
            # ''') 


    def ask_for_confirmation(self, action, entity): 
        entity_dict = { 
            'dept': 'ce département', 
            'user': 'lcet utilisateur',
            'client': 'ce client', 
            'contract': 'ce contrat', 
            'event': 'cet événement'
        } 
        confirmation = session.prompt(f'\nëtes-vous sûr de vouloir {action} {entity} ? (Y/N)') 
        return confirmation 







