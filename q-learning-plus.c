/**
 *  \file   q-learning-plus.c
 *  \brief  Q-Learning Plus Protocol
 *  \author Luis Antonio Costa
 *  \date   2020
 **/
#include <stdio.h>
#include <include/modelutils.h>


/* ************************************************** */
/* ************************************************** */

/* Defining module informations*/
model_t model =  {
    "Q-Learning protocol",
    "Luis Antonio Costa",
    "0.1",
    MODELTYPE_APPLICATION, 
    {NULL, 0}
};


/* ************************************************** */
/* ************************************************** */

/* Defining node type */
#define SENSOR 0
#define SOURCE 1
#define GROUND 2

/* ************************************************** */
/* ************************************************** */

/* Node private data */
struct nodedata {
  int *overhead;
  int type;
  int seq;
  uint64_t period;  
  int last_seq;
  /* for stats */
  int packet_tx;
  int packet_rx;
  int q_value;
};

/* Entity private data */
struct entitydata {
  double p;
  double q;
};


/* ************************************************** */
/* ************************************************** */

/* Data Packet header */
struct packet_header {
  int  source;
  int  seq;
};

/* Location Aquisition function */
void location_aquistion(){
}

/* Routing neighbor discovery function */
void neighbor_discovery(){
}

/* Q-Learning Plus */
int q_learning_plus(){
	return 0
}

/* Routing decision function */
void routing_decision(){
}

/* Penalty mechanism */
void penalty(){
}

/*
 * Phase 1: Location Aquisition
 * **************************************************
 * if (the time of updating node location arrives){
 * 	each node obtains its location via GPS
 * }
 * 
 * Phase 2: Routing neighbor discovery
 * **************************************************
 * if (the time of sending HELLO packets arrives){
 * 	each node sends a HELLO packet;
 * 	These nodes receiving HELLO packets reconfirm their
 *  neighbors and update neighbor tables according to
 *  HELLO packets.
 * }
 * 
 * Phase 3: Routing decision
 * **************************************************
 * while (Data packets need to be sent){
 * 	if (the set of candidate neighbors is not empty){
 *  	Make routing decision based on Q-Learning;
 *  else
 * 		if (there are neighbors whose actual velocity is greater than 0)
 * 			Select the neighbor associated with the maximum actual velocity;
 * 		else
 * 			Penalty mechanism;
 *   }
 * }
 * 
 * Phase 4: Q-Learning
 * **************************************************
 * if (No info about neighbors){
 * 	Initialize the Q-value of each neighbor;
 * }
 * Select the neighbor associated with the largest k-weight Q-value;
 * if (a neighbor is selected to forward data packets){
 * 	Update Q-value of the neighbor by reward;
 * }
 * 
 * Phase 5: Penalty mechanism
 * **************************************************
 * if (the routing hole problem is encountered) OR (forwarding nodes do not receive ACK packets){
 * 	Give minimum reward to related neighbors;
 *  Update Q-value of related neighbors;
 * }
 * /
 * 
 * In this scenario:
 * 
 * Agent: packet
 * State: nodes
 * Action: packet from node i moving to neighbor j
 * 
 * Q-Table must be initialized with random values:
 * each columm defines an action, and each row defines a state
 * therefore, each cell is Q(s,a)
 * 
 * For example, when a packet is at node i, the current
state associated with this packet is s_i. An action a i_j represents
the decision of the packet (agent) to be forwarded from node
i to neighbor node j. By this action, the state of the agent
moves from s_i to s_j and the agent receives a reward about the
action.
 * 
 
/* ************************************************** */
/* ************************************************** */
int callmeback(call_t *c, void *args);


/* ************************************************** */
/* ************************************************** */

/* Here we read the entity variables from the xml config file*/
int init(call_t *c, void *params) {
  struct entitydata *entitydata = malloc(sizeof(struct entitydata));
  param_t *param;

  /* init entity variables */
  entitydata->p = 1;
  entitydata->q = 1;

  /* reading the "init" markup from the xml config file */
  das_init_traverse(params);
  while ((param = (param_t *) das_traverse(params)) != NULL) {

        if (!strcmp(param->key, "p")) {
	  if (get_param_double_range(param->value, &(entitydata->p), 0, 1)) {
	      goto error;
	  }
        } 
        if (!strcmp(param->key, "q")) {
	  if (get_param_double_range(param->value, &(entitydata->q), 0, 1)) {
	      goto error;
	  }
        }
  }
 
  set_entity_private_data(c, entitydata);
  return 0;


error:
    free(entitydata);
    return -1;

}

int destroy(call_t *c) {
    return 0;
}


/* ************************************************** */
/* ************************************************** */

/* Here we read the node variables from the xml config file*/
int setnode(call_t *c, void *params) {
    struct nodedata *nodedata = malloc(sizeof(struct nodedata));
    int i = get_entity_links_down_nbr(c);
    param_t *param;
    
    /* default values */
    nodedata->period    = 1000000000;
    nodedata->type      = SENSOR;
    nodedata->seq       = 0;
    nodedata->last_seq  = -1;
    nodedata->packet_tx = 0;
    nodedata->packet_rx = 0;
    nodedata->q_value   = 0;

    /* reading the "default" markup from the xml config file */
    das_init_traverse(params);
    while ((param = (param_t *) das_traverse(params)) != NULL) {

        if (!strcmp(param->key, "type")) {
            if (get_param_integer(param->value, &(nodedata->type))) {
	        goto error;
            }
        }
        if (!strcmp(param->key, "period")) {
            if (get_param_time(param->value, &(nodedata->period))) {
                goto error;
            }
        }
    }
    
    /* alloc overhead memory */
    if (i) {
        nodedata->overhead = malloc(sizeof(int) * i);
    } else {
        nodedata->overhead = NULL;
    }
    
    set_node_private_data(c, nodedata);
    return 0;

 error:
    free(nodedata);
    return -1;
}

/* Function called at the node's death to unbind the application entity from the node */
int unsetnode(call_t *c) {
    struct nodedata *nodedata = get_node_private_data(c);

    /* we print node stats before exit */
    if (nodedata->packet_tx > 0 || nodedata->packet_rx > 0) {
      printf("[UNSETNODE] Node %d type %d => total rx = %d , total tx = %d \n", c->node, nodedata->type, nodedata->packet_rx, nodedata->packet_tx);
    }

    if (nodedata->overhead) {
        free(nodedata->overhead);
    }
    free(nodedata);
    return 0;
}


/* ************************************************** */
/* ************************************************** */
/* Function called automatically at the node birth */
int bootstrap(call_t *c) {
    struct nodedata *nodedata = get_node_private_data(c);
    int i = get_entity_links_down_nbr(c);
    entityid_t *down = get_entity_links_down(c);
  
    while (i--) {
        call_t c0 = {down[i], c->node};
        
        if ((get_entity_type(&c0) != MODELTYPE_ROUTING) 
            && (get_entity_type(&c0) != MODELTYPE_MAC)) {
            nodedata->overhead[i] = 0;
        } else {
            nodedata->overhead[i] = GET_HEADER_SIZE(&c0);
        }
    }
    
    /* if the node type is source, we schedule a new callback */
    if (nodedata->type != 0) {
      scheduler_add_callback(nodedata->period, c, callmeback, NULL);
    }

    return 0;
}

int ioctl(call_t *c, int option, void *in, void **out) {
    return 0;
}


/* ************************************************** */
/* ************************************************** */
int callmeback(call_t *c, void *args) {
    struct nodedata *nodedata = get_node_private_data(c);

    /* broadcast a new data packet */
    entityid_t *down = get_entity_links_down(c);
    call_t c0 = {down[0], c->node};

    destination_t destination = {BROADCAST_ADDR, {-1, -1, -1}};
    packet_t *packet = packet_alloc(c, nodedata->overhead[0] + sizeof(struct packet_header));
    struct packet_header *header = (struct packet_header *) (packet->data + nodedata->overhead[0]);

    header->source = c->node;
    header->seq    = nodedata->seq++;

    if (SET_HEADER(&c0, packet, &destination) == -1) {
            packet_dealloc(packet);
	    return -1;
    }
        
    printf("[SOURCE] Node %d (%lf %lf) broadcast a packet, seq=%d \n", c->node, get_node_position(c->node)->x, get_node_position(c->node)->y, nodedata->seq);

    TX(&c0, packet);
    
    /* for stats */
    nodedata->packet_tx++;

    /* we schedule a new callback after actualtime+period */
    scheduler_add_callback(get_time() + nodedata->period, c, callmeback, NULL);
    return 0;
}



/* ************************************************** */
/* ************************************************** */
void rx(call_t *c, packet_t *packet) {
    struct nodedata *nodedata = get_node_private_data(c);
    struct entitydata *entitydata = get_entity_private_data(c);

    struct packet_header *header = (struct packet_header *) (packet->data + nodedata->overhead[0]);

    printf("[RX] Node %d (%lf %lf) received a packet from %d sequence = %d !\n", c->node, get_node_position(c->node)->x, get_node_position(c->node)->y, header->source, header->seq);
    
    /* stores the received data according to the q probability */
    if ( get_random_double_range(0.0,1.0) <= entitydata->q ) {
      nodedata->packet_rx++;
    }
    
    /* forwards the received data according to the p probability and if it's a new data */
    if ( (nodedata->last_seq < header->seq) && (get_random_double_range(0.0,1.0) <= entitydata->p) ) {    
      entityid_t *down = get_entity_links_down(c);
      call_t c0 = {down[0], c->node};     

      nodedata->last_seq = header->seq;
      TX(&c0, packet);
      
      nodedata->packet_tx++;
      
      printf("[TX] Node %d (%lf %lf) sent a packet sequence = %d !\n", c->node, get_node_position(c->node)->x, get_node_position(c->node)->y, header->source, header->seq);
      
      return;
    }

    /* else dealloc the packet */
    packet_dealloc(packet);
}


/* ************************************************** */
/* ************************************************** */
application_methods_t methods = {rx};
