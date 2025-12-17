"""
Ruby on Rails framework tasks with detailed expert-level instructions.
Based on Rails Doctrine and community best practices.
"""
from typing import Dict, List
from crewai import Agent, Task
from frameworks.base import BaseTasks


class RailsTasks(BaseTasks):
    """Factory for Rails-specific tasks with comprehensive instructions."""
    
    @property
    def framework_name(self) -> str:
        return "Ruby on Rails"
    
    def rails_architecture_task(self, agent: Agent, analysis: Dict) -> Task:
        return self.create_architecture_task(
            agent=agent,
            analysis=analysis,
            description="""\
                Design a Rails architecture following the Rails Doctrine.
                
                **REQUIREMENTS:**
                {requirements}
                
                **FILES TO MODIFY:** {files_to_modify}
                **FILES TO CREATE:** {files_to_create}
                
                ---
                
                **DELIVERABLES:**
                
                1. **Database Schema Design**
                   ```ruby
                   # For each model, define:
                   create_table :table_name do |t|
                     t.references :foreign_key, null: false, foreign_key: true
                     t.string :column_name, null: false
                     t.timestamps
                     
                     t.index :column_name  # Add indexes for search/filter columns
                   end
                   ```
                
                2. **Model Specifications**
                   ```
                   ModelName:
                     Purpose: [single responsibility]
                     Associations:
                       - belongs_to :parent
                       - has_many :children
                     Validations:
                       - presence: [:field1, :field2]
                       - uniqueness: [:email]
                     Scopes:
                       - active: where(active: true)
                     Methods:
                       - business_method: description
                   ```
                
                3. **Controller Structure**
                   ```
                   ControllerName:
                     Actions: [index, show, create, update, destroy]
                     Before Actions:
                       - authenticate_user!
                       - set_resource
                     Strong Params: [:permitted, :fields]
                   ```
                
                4. **Routes Design**
                   ```ruby
                   Rails.application.routes.draw do
                     namespace :api do
                       namespace :v1 do
                         resources :resource_name do
                           collection do
                             get :search
                           end
                           member do
                             post :action
                           end
                         end
                       end
                     end
                   end
                   ```
                
                5. **Service Objects (if needed)**
                   ```
                   ServiceName:
                     Purpose: [complex operation]
                     Dependencies: [external services]
                     Input: [parameters]
                     Output: Result object with success/failure
                   ```
                
                6. **Background Jobs**
                   ```
                   JobName:
                     Queue: [default/mailers/low_priority]
                     Trigger: [when it runs]
                     Retries: [retry strategy]
                   ```
                
                {incentive}""",
            expected_output="""\
                Complete Rails architecture document with:
                - Database schema with migrations
                - Model specifications with associations
                - RESTful controller structure
                - Routes configuration
                - Service objects for complex logic
                - Background job specifications""",
        )
    
    def rails_implementation_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_implementation_task(
            agent=agent,
            context=context,
            description="""\
                Implement Rails features following the architecture design.
                
                **IMPLEMENTATION STANDARDS:**
                
                1. **Migrations**
                   ```ruby
                   class CreateOrders < ActiveRecord::Migration[7.0]
                     def change
                       create_table :orders do |t|
                         t.references :user, null: false, foreign_key: true
                         t.decimal :total, precision: 10, scale: 2, null: false
                         t.string :status, default: 'pending', null: false
                         t.timestamps
                         
                         t.index :status
                         t.index [:user_id, :created_at]
                       end
                     end
                   end
                   ```
                
                2. **Models**
                   ```ruby
                   class Order < ApplicationRecord
                     # Associations
                     belongs_to :user
                     has_many :line_items, dependent: :destroy
                     has_many :products, through: :line_items
                     
                     # Validations
                     validates :total, presence: true,
                                       numericality: { greater_than_or_equal_to: 0 }
                     validates :status, inclusion: { in: STATUSES }
                     
                     # Scopes
                     scope :recent, -> { order(created_at: :desc) }
                     scope :by_status, ->(status) { where(status: status) }
                     
                     # Callbacks (use sparingly)
                     after_create_commit :notify_admin
                     
                     # Instance methods
                     def complete!
                       transaction do
                         update!(status: 'completed', completed_at: Time.current)
                         line_items.each(&:fulfill!)
                       end
                     end
                     
                     private
                     
                     def notify_admin
                       AdminNotificationJob.perform_later(id)
                     end
                   end
                   ```
                
                3. **Controllers**
                   ```ruby
                   module Api
                     module V1
                       class OrdersController < BaseController
                         before_action :authenticate_user!
                         before_action :set_order, only: %i[show update destroy]
                         
                         def index
                           @orders = current_user.orders
                                                  .includes(:line_items)
                                                  .recent
                                                  .page(params[:page])
                           
                           render json: OrderSerializer.new(@orders)
                         end
                         
                         def create
                           @order = current_user.orders.build(order_params)
                           
                           if @order.save
                             render json: OrderSerializer.new(@order), status: :created
                           else
                             render json: ErrorSerializer.new(@order), status: :unprocessable_entity
                           end
                         end
                         
                         private
                         
                         def set_order
                           @order = current_user.orders.find(params[:id])
                         end
                         
                         def order_params
                           params.require(:order).permit(
                             :shipping_address,
                             line_items_attributes: %i[product_id quantity]
                           )
                         end
                       end
                     end
                   end
                   ```
                
                4. **Service Objects**
                   ```ruby
                   module Orders
                     class ProcessPayment
                       Result = Struct.new(:success?, :order, :error, keyword_init: true)
                       
                       def initialize(order, payment_method)
                         @order = order
                         @payment_method = payment_method
                       end
                       
                       def call
                         return failure('Order is invalid') unless @order.valid?
                         return failure('Already paid') if @order.paid?
                         
                         ActiveRecord::Base.transaction do
                           charge = create_charge
                           @order.update!(payment_id: charge.id, status: 'paid')
                         end
                         
                         success(@order)
                       rescue PaymentGateway::Error => e
                         failure(e.message)
                       end
                       
                       private
                       
                       def create_charge
                         PaymentGateway.charge(
                           amount: @order.total,
                           method: @payment_method
                         )
                       end
                       
                       def success(order)
                         Result.new(success?: true, order: order)
                       end
                       
                       def failure(error)
                         Result.new(success?: false, error: error)
                       end
                     end
                   end
                   ```
                
                5. **Background Jobs**
                   ```ruby
                   class ProcessOrderJob < ApplicationJob
                     queue_as :default
                     
                     retry_on ActiveRecord::Deadlocked, wait: 5.seconds, attempts: 3
                     discard_on ActiveJob::DeserializationError
                     
                     def perform(order_id)
                       order = Order.find(order_id)
                       result = Orders::ProcessPayment.new(order, order.payment_method).call
                       
                       unless result.success?
                         Rails.logger.error("Payment failed: #{result.error}")
                       end
                     end
                   end
                   ```""",
            expected_output="""\
                Complete Rails implementation including:
                - Database migrations with proper indexes
                - Models with validations and associations
                - RESTful controllers with strong params
                - Service objects for complex logic
                - Background jobs for async operations
                - Serializers for JSON responses""",
        )
    
    def rails_testing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_testing_task(
            agent=agent,
            context=context,
            description="""\
                Write comprehensive RSpec tests for the Rails implementation.
                
                **TESTING REQUIREMENTS:**
                
                1. **Model Specs**
                   ```ruby
                   RSpec.describe Order, type: :model do
                     describe 'associations' do
                       it { is_expected.to belong_to(:user) }
                       it { is_expected.to have_many(:line_items).dependent(:destroy) }
                     end
                     
                     describe 'validations' do
                       it { is_expected.to validate_presence_of(:total) }
                       it { is_expected.to validate_numericality_of(:total) }
                     end
                     
                     describe 'scopes' do
                       describe '.recent' do
                         it 'orders by created_at desc' do
                           old_order = create(:order, created_at: 1.day.ago)
                           new_order = create(:order, created_at: 1.hour.ago)
                           
                           expect(Order.recent).to eq([new_order, old_order])
                         end
                       end
                     end
                     
                     describe '#complete!' do
                       let(:order) { create(:order, :with_line_items) }
                       
                       it 'updates status to completed' do
                         order.complete!
                         expect(order.reload.status).to eq('completed')
                       end
                       
                       it 'sets completed_at timestamp' do
                         freeze_time do
                           order.complete!
                           expect(order.completed_at).to eq(Time.current)
                         end
                       end
                     end
                   end
                   ```
                
                2. **Request Specs**
                   ```ruby
                   RSpec.describe 'Orders API', type: :request do
                     let(:user) { create(:user) }
                     let(:headers) { auth_headers_for(user) }
                     
                     describe 'GET /api/v1/orders' do
                       before { create_list(:order, 3, user: user) }
                       
                       it 'returns user orders' do
                         get '/api/v1/orders', headers: headers
                         
                         expect(response).to have_http_status(:ok)
                         expect(json_body['data'].size).to eq(3)
                       end
                       
                       it 'does not return other users orders' do
                         other_order = create(:order)
                         get '/api/v1/orders', headers: headers
                         
                         order_ids = json_body['data'].pluck('id')
                         expect(order_ids).not_to include(other_order.id)
                       end
                     end
                     
                     describe 'POST /api/v1/orders' do
                       let(:product) { create(:product) }
                       let(:valid_params) do
                         {
                           order: {
                             line_items_attributes: [
                               { product_id: product.id, quantity: 2 }
                             ]
                           }
                         }
                       end
                       
                       context 'with valid params' do
                         it 'creates order' do
                           expect {
                             post '/api/v1/orders', params: valid_params, headers: headers
                           }.to change(Order, :count).by(1)
                         end
                         
                         it 'returns created status' do
                           post '/api/v1/orders', params: valid_params, headers: headers
                           expect(response).to have_http_status(:created)
                         end
                       end
                       
                       context 'without authentication' do
                         it 'returns unauthorized' do
                           post '/api/v1/orders', params: valid_params
                           expect(response).to have_http_status(:unauthorized)
                         end
                       end
                     end
                   end
                   ```
                
                3. **Service Specs**
                   ```ruby
                   RSpec.describe Orders::ProcessPayment do
                     let(:order) { create(:order, total: 100.00) }
                     let(:payment_method) { 'card_token_123' }
                     
                     subject { described_class.new(order, payment_method).call }
                     
                     context 'with valid payment' do
                       before do
                         allow(PaymentGateway).to receive(:charge)
                           .and_return(OpenStruct.new(id: 'ch_123'))
                       end
                       
                       it 'returns success' do
                         expect(subject.success?).to be true
                       end
                       
                       it 'updates order status' do
                         subject
                         expect(order.reload.status).to eq('paid')
                       end
                     end
                     
                     context 'with payment failure' do
                       before do
                         allow(PaymentGateway).to receive(:charge)
                           .and_raise(PaymentGateway::Error, 'Card declined')
                       end
                       
                       it 'returns failure' do
                         expect(subject.success?).to be false
                         expect(subject.error).to eq('Card declined')
                       end
                     end
                   end
                   ```
                
                4. **Factory Definitions**
                   ```ruby
                   FactoryBot.define do
                     factory :order do
                       user
                       total { Faker::Commerce.price(range: 10..500.0) }
                       status { 'pending' }
                       
                       trait :completed do
                         status { 'completed' }
                         completed_at { Time.current }
                       end
                       
                       trait :with_line_items do
                         after(:create) do |order|
                           create_list(:line_item, 2, order: order)
                         end
                       end
                     end
                   end
                   ```""",
            expected_output="""\
                Complete RSpec test suite including:
                - Model specs with validations and associations
                - Request specs for all API endpoints
                - Service object specs with mocked dependencies
                - FactoryBot factories with traits
                - Shared examples for common behavior
                - 90%+ code coverage""",
        )
    
    def rails_reviewing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_review_task(
            agent=agent,
            context=context,
            description="""\
                Review Rails implementation for production readiness.
                
                **REVIEW CHECKLIST:**
                
                1. **Rails Conventions**
                   □ RESTful routes (7 standard actions)
                   □ Fat models, skinny controllers
                   □ Proper use of concerns
                   □ Naming conventions followed
                   □ Rails helpers utilized
                
                2. **Database & Performance**
                   □ No N+1 queries (check with Bullet gem)
                   □ Indexes on foreign keys
                   □ Indexes on search columns
                   □ Large datasets paginated
                   □ Expensive operations backgrounded
                   □ Counter caches where needed
                
                3. **Security**
                   □ Strong parameters used
                   □ Authorization on all actions
                   □ No mass assignment vulnerabilities
                   □ SQL injection prevented
                   □ XSS prevented
                   □ CSRF protection enabled
                   □ Sensitive data encrypted
                
                4. **Code Quality**
                   □ Single responsibility principle
                   □ No god classes
                   □ Meaningful names
                   □ No dead code
                   □ Proper error handling
                
                5. **Testing**
                   □ Model validations tested
                   □ API endpoints tested
                   □ Edge cases covered
                   □ Factories realistic
                
                **PROVIDE:**
                - Issues with severity (Critical/Major/Minor)
                - Specific fix recommendations
                - Performance suggestions
                - Security assessment
                - Deployment instructions""",
            expected_output="""\
                Comprehensive review report including:
                - Categorized issues with fixes
                - Performance recommendations
                - Security assessment
                - Database optimization suggestions
                - Deployment checklist
                - Commands to run the application""",
        )
