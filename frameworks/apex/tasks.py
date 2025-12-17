"""
Salesforce Apex framework tasks with detailed expert-level instructions.
Based on Salesforce official documentation and ISV best practices.
"""
from typing import Dict, List
from crewai import Agent, Task
from frameworks.base import BaseTasks


class ApexTasks(BaseTasks):
    """Factory for Apex-specific tasks with comprehensive instructions."""
    
    @property
    def framework_name(self) -> str:
        return "Salesforce Apex"
    
    def apex_architecture_task(self, agent: Agent, analysis: Dict) -> Task:
        return self.create_architecture_task(
            agent=agent,
            analysis=analysis,
            description="""\
                Design Salesforce architecture respecting Governor Limits.
                
                **REQUIREMENTS:**
                {requirements}
                
                **FILES TO MODIFY:** {files_to_modify}
                **FILES TO CREATE:** {files_to_create}
                
                ---
                
                **DELIVERABLES:**
                
                1. **Data Model Design**
                   ```
                   Object: Object_Name__c
                   Purpose: [description]
                   Fields:
                     - Field_Name__c (Type, Required, Indexed)
                   Relationships:
                     - Parent: Master-Detail/Lookup to Object
                     - Children: Related objects
                   Validation Rules:
                     - Rule name and criteria
                   ```
                
                2. **Trigger Framework**
                   ```
                   Trigger: ObjectTrigger
                   Events: before insert, after insert, before update, after update
                   Handler: ObjectTriggerHandler
                   Service: ObjectService
                   Selector: ObjectSelector
                   ```
                
                3. **Service Layer Design**
                   ```
                   Service: ServiceName
                   Methods:
                     - methodName(params): returnType
                       Purpose: [description]
                       Bulkified: Yes/No
                       Governor Limit Impact: [SOQL: X, DML: Y]
                   ```
                
                4. **SOQL Query Plan**
                   ```
                   Query: queryName
                   Purpose: [what data it retrieves]
                   Fields: [selected fields]
                   Filters: [WHERE conditions - must use indexed fields]
                   Relationships: [related objects to query]
                   Expected Records: [estimate]
                   ```
                
                5. **Governor Limits Analysis**
                   ```
                   Operation: [operation name]
                   SOQL Queries: X of 100
                   DML Statements: Y of 150
                   Records Retrieved: Z of 50,000
                   Heap Size Impact: [estimate]
                   Async Processing: Required/Not Required
                   ```
                
                6. **Security Model**
                   ```
                   Sharing: with sharing / without sharing / inherited sharing
                   CRUD Requirements: Create, Read, Update, Delete
                   FLS Requirements: Fields that need access checks
                   Permission Sets: Required permissions
                   ```
                
                {incentive}""",
            expected_output="""\
                Complete Salesforce architecture document with:
                - Data model with objects and relationships
                - Trigger framework specification
                - Service layer methods with governor limit analysis
                - Optimized SOQL query plans
                - Security model with sharing rules
                - Deployment checklist""",
        )
    
    def apex_implementation_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_implementation_task(
            agent=agent,
            context=context,
            description="""\
                Implement Apex code following architecture and Governor Limits.
                
                **IMPLEMENTATION STANDARDS:**
                
                1. **Trigger (One Per Object)**
                   ```apex
                   trigger AccountTrigger on Account (
                       before insert, before update, before delete,
                       after insert, after update, after delete, after undelete
                   ) {
                       TriggerDispatcher.run(new AccountTriggerHandler());
                   }
                   ```
                
                2. **Trigger Handler**
                   ```apex
                   public class AccountTriggerHandler implements ITriggerHandler {
                       
                       public void beforeInsert(List<SObject> newList) {
                           AccountService.setDefaults((List<Account>)newList);
                       }
                       
                       public void afterInsert(List<SObject> newList) {
                           AccountService.createRelatedRecords((List<Account>)newList);
                       }
                       
                       public void beforeUpdate(List<SObject> newList, Map<Id, SObject> oldMap) {
                           AccountService.validateChanges(
                               (List<Account>)newList, 
                               (Map<Id, Account>)oldMap
                           );
                       }
                       
                       // Implement other events as needed
                   }
                   ```
                
                3. **Service Class (Bulkified)**
                   ```apex
                   public with sharing class AccountService {
                       
                       public static void setDefaults(List<Account> accounts) {
                           for (Account acc : accounts) {
                               if (acc.Status__c == null) {
                                   acc.Status__c = 'New';
                               }
                           }
                       }
                       
                       public static void createRelatedRecords(List<Account> accounts) {
                           List<Contact> contactsToInsert = new List<Contact>();
                           
                           for (Account acc : accounts) {
                               contactsToInsert.add(new Contact(
                                   AccountId = acc.Id,
                                   LastName = 'Primary Contact',
                                   Email = 'primary@' + acc.Id + '.com'
                               ));
                           }
                           
                           if (!contactsToInsert.isEmpty()) {
                               insert contactsToInsert;
                           }
                       }
                       
                       public static void processWithRelatedData(Set<Id> accountIds) {
                           // Single query to get all needed data
                           List<Account> accounts = AccountSelector.selectWithContacts(accountIds);
                           
                           List<Task> tasksToCreate = new List<Task>();
                           List<Account> accountsToUpdate = new List<Account>();
                           
                           for (Account acc : accounts) {
                               // Process each account
                               acc.Last_Processed__c = DateTime.now();
                               accountsToUpdate.add(acc);
                               
                               // Process related contacts
                               for (Contact c : acc.Contacts) {
                                   tasksToCreate.add(new Task(
                                       WhatId = acc.Id,
                                       WhoId = c.Id,
                                       Subject = 'Follow up'
                                   ));
                               }
                           }
                           
                           // Bulk DML
                           if (!accountsToUpdate.isEmpty()) {
                               update accountsToUpdate;
                           }
                           if (!tasksToCreate.isEmpty()) {
                               insert tasksToCreate;
                           }
                       }
                   }
                   ```
                
                4. **Selector Class**
                   ```apex
                   public inherited sharing class AccountSelector {
                       
                       public static List<Account> selectById(Set<Id> ids) {
                           return [
                               SELECT Id, Name, Industry, Status__c, OwnerId
                               FROM Account
                               WHERE Id IN :ids
                               WITH SECURITY_ENFORCED
                           ];
                       }
                       
                       public static List<Account> selectWithContacts(Set<Id> ids) {
                           return [
                               SELECT Id, Name, Industry,
                                      (SELECT Id, FirstName, LastName, Email 
                                       FROM Contacts
                                       ORDER BY CreatedDate DESC)
                               FROM Account
                               WHERE Id IN :ids
                               WITH SECURITY_ENFORCED
                           ];
                       }
                       
                       public static List<Account> selectByIndustry(String industry, Integer limitCount) {
                           return [
                               SELECT Id, Name, Industry, BillingCity
                               FROM Account
                               WHERE Industry = :industry
                               WITH SECURITY_ENFORCED
                               ORDER BY Name
                               LIMIT :limitCount
                           ];
                       }
                   }
                   ```
                
                5. **Batch Apex (For Large Data Volumes)**
                   ```apex
                   public class AccountBatchProcessor implements Database.Batchable<SObject>, Database.Stateful {
                       
                       private Integer successCount = 0;
                       private Integer errorCount = 0;
                       
                       public Database.QueryLocator start(Database.BatchableContext bc) {
                           return Database.getQueryLocator([
                               SELECT Id, Name, Status__c
                               FROM Account
                               WHERE Status__c = 'Pending'
                               WITH SECURITY_ENFORCED
                           ]);
                       }
                       
                       public void execute(Database.BatchableContext bc, List<Account> scope) {
                           List<Account> toUpdate = new List<Account>();
                           
                           for (Account acc : scope) {
                               acc.Status__c = 'Processed';
                               acc.Processed_Date__c = Date.today();
                               toUpdate.add(acc);
                           }
                           
                           Database.SaveResult[] results = Database.update(toUpdate, false);
                           for (Database.SaveResult sr : results) {
                               if (sr.isSuccess()) {
                                   successCount++;
                               } else {
                                   errorCount++;
                               }
                           }
                       }
                       
                       public void finish(Database.BatchableContext bc) {
                           // Send notification or log results
                           System.debug('Success: ' + successCount + ', Errors: ' + errorCount);
                       }
                   }
                   ```
                
                6. **Error Handling**
                   ```apex
                   public class AccountException extends Exception {}
                   
                   public static void processWithErrorHandling(List<Account> accounts) {
                       Savepoint sp = Database.setSavepoint();
                       
                       try {
                           validateAccounts(accounts);
                           processAccounts(accounts);
                       } catch (DmlException e) {
                           Database.rollback(sp);
                           throw new AccountException('Processing failed: ' + e.getMessage());
                       } catch (Exception e) {
                           Database.rollback(sp);
                           // Log error
                           ErrorLogger.log(e, 'AccountService.processWithErrorHandling');
                           throw e;
                       }
                   }
                   ```""",
            expected_output="""\
                Complete Apex implementation including:
                - Triggers with handler pattern
                - Bulkified service classes
                - Selector classes with secure queries
                - Batch/Queueable classes for async processing
                - Custom exceptions and error handling
                - All code respects Governor Limits""",
        )
    
    def apex_testing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_testing_task(
            agent=agent,
            context=context,
            description="""\
                Write comprehensive Apex test classes with 90%+ coverage.
                
                **TESTING REQUIREMENTS:**
                
                1. **Test Data Factory**
                   ```apex
                   @isTest
                   public class TestDataFactory {
                       
                       public static List<Account> createAccounts(Integer count) {
                           List<Account> accounts = new List<Account>();
                           for (Integer i = 0; i < count; i++) {
                               accounts.add(new Account(
                                   Name = 'Test Account ' + i,
                                   Industry = 'Technology',
                                   BillingCity = 'San Francisco',
                                   Status__c = 'New'
                               ));
                           }
                           return accounts;
                       }
                       
                       public static List<Contact> createContacts(List<Account> accounts) {
                           List<Contact> contacts = new List<Contact>();
                           for (Account acc : accounts) {
                               contacts.add(new Contact(
                                   FirstName = 'Test',
                                   LastName = 'Contact',
                                   AccountId = acc.Id,
                                   Email = 'test@example.com'
                               ));
                           }
                           return contacts;
                       }
                   }
                   ```
                
                2. **Trigger Test (Bulk)**
                   ```apex
                   @isTest
                   private class AccountTriggerTest {
                       
                       @isTest
                       static void testBulkInsert_ShouldSetDefaults() {
                           // Arrange - Test with 200 records
                           List<Account> accounts = TestDataFactory.createAccounts(200);
                           
                           // Act
                           Test.startTest();
                           insert accounts;
                           Test.stopTest();
                           
                           // Assert
                           List<Account> inserted = [SELECT Id, Status__c FROM Account];
                           System.assertEquals(200, inserted.size());
                           for (Account acc : inserted) {
                               System.assertEquals('New', acc.Status__c);
                           }
                       }
                       
                       @isTest
                       static void testBulkUpdate_ShouldValidateChanges() {
                           // Arrange
                           List<Account> accounts = TestDataFactory.createAccounts(200);
                           insert accounts;
                           
                           for (Account acc : accounts) {
                               acc.Status__c = 'Active';
                           }
                           
                           // Act
                           Test.startTest();
                           update accounts;
                           Test.stopTest();
                           
                           // Assert
                           List<Account> updated = [SELECT Id, Status__c FROM Account];
                           for (Account acc : updated) {
                               System.assertEquals('Active', acc.Status__c);
                           }
                       }
                   }
                   ```
                
                3. **Service Test**
                   ```apex
                   @isTest
                   private class AccountServiceTest {
                       
                       @TestSetup
                       static void setup() {
                           List<Account> accounts = TestDataFactory.createAccounts(10);
                           insert accounts;
                       }
                       
                       @isTest
                       static void testProcessWithRelatedData_ShouldCreateTasks() {
                           // Arrange
                           List<Account> accounts = [SELECT Id FROM Account];
                           List<Contact> contacts = TestDataFactory.createContacts(accounts);
                           insert contacts;
                           
                           Set<Id> accountIds = new Map<Id, Account>(accounts).keySet();
                           
                           // Act
                           Test.startTest();
                           AccountService.processWithRelatedData(accountIds);
                           Test.stopTest();
                           
                           // Assert
                           List<Task> tasks = [SELECT Id, WhatId FROM Task];
                           System.assertEquals(10, tasks.size());
                           
                           List<Account> updated = [SELECT Last_Processed__c FROM Account];
                           for (Account acc : updated) {
                               System.assertNotEquals(null, acc.Last_Processed__c);
                           }
                       }
                       
                       @isTest
                       static void testProcessWithRelatedData_NoContacts_ShouldNotFail() {
                           // Arrange - Accounts without contacts
                           List<Account> accounts = [SELECT Id FROM Account];
                           Set<Id> accountIds = new Map<Id, Account>(accounts).keySet();
                           
                           // Act
                           Test.startTest();
                           AccountService.processWithRelatedData(accountIds);
                           Test.stopTest();
                           
                           // Assert - No tasks created, no errors
                           List<Task> tasks = [SELECT Id FROM Task];
                           System.assertEquals(0, tasks.size());
                       }
                   }
                   ```
                
                4. **Batch Test**
                   ```apex
                   @isTest
                   private class AccountBatchProcessorTest {
                       
                       @isTest
                       static void testBatchExecution() {
                           // Arrange
                           List<Account> accounts = TestDataFactory.createAccounts(50);
                           for (Account acc : accounts) {
                               acc.Status__c = 'Pending';
                           }
                           insert accounts;
                           
                           // Act
                           Test.startTest();
                           Database.executeBatch(new AccountBatchProcessor(), 200);
                           Test.stopTest();
                           
                           // Assert
                           List<Account> processed = [
                               SELECT Status__c, Processed_Date__c 
                               FROM Account
                           ];
                           for (Account acc : processed) {
                               System.assertEquals('Processed', acc.Status__c);
                               System.assertEquals(Date.today(), acc.Processed_Date__c);
                           }
                       }
                   }
                   ```
                
                5. **Negative Test Cases**
                   ```apex
                   @isTest
                   static void testValidation_InvalidData_ShouldThrowException() {
                       // Arrange
                       Account acc = new Account(Name = ''); // Invalid
                       
                       // Act & Assert
                       Test.startTest();
                       try {
                           insert acc;
                           System.assert(false, 'Exception expected');
                       } catch (DmlException e) {
                           System.assert(e.getMessage().contains('REQUIRED_FIELD_MISSING'));
                       }
                       Test.stopTest();
                   }
                   ```""",
            expected_output="""\
                Complete Apex test suite including:
                - TestDataFactory for reusable test data
                - Bulk trigger tests (200 records)
                - Service class tests with assertions
                - Batch/Queueable tests
                - Positive and negative test cases
                - 90%+ code coverage""",
        )
    
    def apex_reviewing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_review_task(
            agent=agent,
            context=context,
            description="""\
                Review Salesforce implementation for deployment readiness.
                
                **REVIEW CHECKLIST:**
                
                1. **Governor Limits (CRITICAL)**
                   □ No SOQL in loops
                   □ No DML in loops
                   □ Queries use indexed fields
                   □ LIMIT clauses where appropriate
                   □ Collections for bulk processing
                   □ Async for heavy processing
                
                2. **Bulkification**
                   □ Handles 200+ records
                   □ Maps for efficient lookups
                   □ Single query for all data
                   □ Single DML for all records
                
                3. **Security (CRITICAL)**
                   □ WITH SECURITY_ENFORCED in SOQL
                   □ CRUD checks before DML
                   □ FLS checks before field access
                   □ Proper sharing keywords
                   □ No hardcoded IDs
                   □ No SOQL injection
                
                4. **Code Quality**
                   □ One trigger per object
                   □ Handler pattern used
                   □ Service/Selector separation
                   □ Meaningful names
                   □ Error handling
                   □ No System.debug in production
                
                5. **Testing**
                   □ 75%+ coverage (aim 90%+)
                   □ Bulk tests included
                   □ Test.startTest/stopTest used
                   □ Meaningful assertions
                   □ Negative test cases
                
                6. **Deployment Checklist**
                   □ All tests pass
                   □ No validation errors
                   □ Permission sets defined
                   □ Custom settings configured
                
                **PROVIDE:**
                - Governor limit analysis
                - Security vulnerabilities
                - Code quality issues
                - Test coverage report
                - Deployment commands (sfdx)""",
            expected_output="""\
                Comprehensive review report including:
                - Governor limit compliance status
                - Security assessment
                - Bulkification verification
                - Code quality score
                - Test coverage percentage
                - SFDX deployment commands""",
        )
