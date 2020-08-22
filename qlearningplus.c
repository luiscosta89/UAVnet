/**
 *  \file   qlearningplus.c
 *  \brief  Q-Learning Plus Protocol
 *  \author Luis Antonio Costa
 *  \date   2020
 **/
#include <stdio.h>
#include <stdlib.h>

#include <include/modelutils.h>

#define MAX 25;
#define ALPHA 0.6;
#define EPSILON 0.1;
#define SW 0.7;

/* **************** GLOBAL VARIABLES **************** */

float epochWeights[10];
bool notACK = FALSE;
bool routingHole = FALSE;


/* ************************************************** */
/* ************************************************** */
model_t model =  {
    "Q-Learning protocol",
    "Luis Antonio Costa",
    "0.1",
    MODELTYPE_APPLICATION, 
    {NULL, 0}
};


/* ************************************************** */
/* ************************************************** */
struct _cbr_private {
    uint64_t start;
    uint64_t period;
    nodeid_t destination;
    position_t position;
    int sequence;
    int overhead;
    void *timer_id;
    /* stats */
	double avg_distance;    /* average distance of discovery */
	double avg_connexity;   /* average connexity */
	double avg_neighbors;   /* average number of discovered neighbors */
	double avg_rx;          /* nbr of received packets */
	double avg_delivery;    /* average delivery ratio */
  
};

/* ************************************************** */
/* ************************************************** */
struct data_packet_header {
    int source;
    int sequence;
    double delay;
    double source_pos_x;
    double source_pos_y;
};

/* ****************** TABLES ************************ */

/* Q-Table */
float qTable[MAX][MAX];


/* R-Table */
float rTable[MAX][MAX]


/* Initialize Tables*/
int i, j;
for (int i=0; i<=MAX; i++) {
	for (int j=0; j<=MAX;i++)
		qTable[MAX][MAX] = 0.5;
		rTable[MAX][MAX] = 0;


/* ************************************************** */

/* Intializes random number generator */
   srand((unsigned) time(&t));
   

/* Initializes the random weights of the last 10 epochs */
void randomWeights() {
	srand((unsigned int)time(NULL));
	
	float sum = 1.0;
	float subSum = sum;    

	for(int i = 0; i < 10 - 2; i++) {
		epochWeights[i] = ((float)rand()/(float)(RAND_MAX)) * subSum; // get random number between 0 and subSum 
		subSum -= epochWeights[i];
    }

	epochWeights[n - 1] = subSum; // leftovers go to the last random number
}

/* Explore any path with any Q-value */
int explore() {
	int path;
	
	path = rand()%25;
	
	return path;
}
	
/* Choose the max Q-value action*/
int exploit() {
	return max;
}
	
/* e-Greedy policy */
void chooseGreedyAction() {
	
	int randomValue = rand()%1;
	
	if (randomValue > EPSILON) {
		return exploit()
	}
	else
		return explore()
}

/* Velocity Constraint */
void velocityConstraint(){
}

/* Reward Function */
float rewardFunction(){
}

/* Calculate the last epochs */
float lastEpocs(int l){
	int i;
	float value = 0;
	
	for(i=0; i<=l; i++){
		value += (weight[i]*reward[i])*a[i]
	}
	
	return value;
}

/* Noise condition */
float noiseCondition(){
	float noise = 0;
	
	if(SINR < 15)
	{
		noise = 0;
	}
	else if (SINR >= 15) && (SINR < 17)
	{
		noise = 0.25;
	}
	else if (SINR >= 17) && (SINR < 20)
	{
		noise = 0.5;
	}
	else if (SINR >= 20) && (SINR < 25)
	{
		noise = 0.75;
	}
	else if (SINR >= 25)
	{
		noise = 1;
	}
	
	return noise;
}

/* Q-value update */
void qValue() {
	
	int c, sum = 0;
	
	for (c=0; c<=10; c++)
	{
		sum = sum + (epochWeights[i][j] * rTable[i][j])
	}
	
	// Update q-value
	qTable[i][j] = (1-ALPHA) * sum + rTable[i][j] + (SW * noiseCondition())
}


/* ************************************************** */
/* ************************************************** */
int send_message(call_t *c, void *args);
void tx(call_t *c);


/* ************************************************** */
/* ************************************************** */
int init(call_t *c, void *params) {
    return 0;
}

int destroy(call_t *c) {
    return 0;
}


/* ************************************************** */
/* ************************************************** */
int setnode(call_t *c, void *params) {
    struct _cbr_private *nodedata = malloc(sizeof(struct _cbr_private));
    param_t *param;
        
    /* default values */
    nodedata->destination = get_random_node(c->node);
    nodedata->position.x = get_random_x_position();
    nodedata->position.y = get_random_y_position();
    nodedata->position.z = get_random_z_position();
    nodedata->start = 0;
    nodedata->period = 1000000000;
    nodedata->sequence = 0;

    /* get parameters */
    das_init_traverse(params);
    while ((param = (param_t *) das_traverse(params)) != NULL) {

        if (!strcmp(param->key, "destination")) {
            if (get_param_nodeid(param->value, &(nodedata->destination), c->node)) {
                goto error;
            }
        }
        if (!strcmp(param->key, "destination-x")) {
            if (get_param_x_position(param->value, &(nodedata->position.x))) {
                goto error;
            }
        }
        if (!strcmp(param->key, "destination-y")) {
            if (get_param_y_position(param->value, &(nodedata->position.y))) {
                goto error;
            }
        }
        if (!strcmp(param->key, "destination-z")) {
            if (get_param_z_position(param->value, &(nodedata->position.z))) {
                goto error;
            }
        }
        if (!strcmp(param->key, "start")) {
            if (get_param_time(param->value, &(nodedata->start))) {
                goto error;
            }
        }
        if (!strcmp(param->key, "period")) {
            if (get_param_time(param->value, &(nodedata->period))) {
                goto error;
            }
        }
    }
    
    set_node_private_data(c, nodedata);
    return 0;
  
 error:
    free(nodedata);
    return -1;
}

int unsetnode(call_t *c) {
    struct _cbr_private *nodedata = get_node_private_data(c);
    free(nodedata);    
    return 0;
}


/* ************************************************** */
/* ************************************************** */
int bootstrap(call_t *c) {
    struct _cbr_private *nodedata = get_node_private_data(c);
    array_t *down = get_entity_bindings_down(c);
    call_t c0 = {down->elts[0], c->node, c->entity};
    uint64_t start = get_time() + nodedata->start + get_random_double() * nodedata->period;
  
    /* get overhead */
    nodedata->overhead = GET_HEADER_SIZE(&c0);
    
    /* create a periodic timer for the function send_message */
    nodedata->timer_id = create_timer(c, send_message, never_stop, periodic_trigger, &(nodedata->period));    

    /* start timer */
    start_timer(nodedata->timer_id, start); 

    return 0;
}

int ioctl(call_t *c, int option, void *in, void **out) {
    return 0;
}


/* ************************************************** */
/* ************************************************** */
int send_message(call_t *c, void *args) {
    tx(c);
    return 0;
}


/* ************************************************** */
/* ************************************************** */
void tx(call_t *c) {
    struct _cbr_private *nodedata = get_node_private_data(c);
    array_t *down = get_entity_bindings_down(c);
    packet_t *packet = packet_create(c, nodedata->overhead + sizeof(struct data_packet_header), -1);

    call_t c0 = {down->elts[0], c->node, c->entity};
    destination_t destination = {nodedata->destination, 
                                 {nodedata->position.x, 
                                  nodedata->position.y, 
                                  nodedata->position.z}};
        
    if (SET_HEADER(&c0, packet, &destination) == -1) {
        packet_dealloc(packet);
        return;
    }

    struct data_packet_header *header = (struct data_packet_header *) (packet->data + nodedata->overhead);
    header->source = c->node;
    header->sequence = nodedata->sequence++;
    header->delay = get_time() * 0.000000001;
    header->source_pos_x = get_node_position(c->node)->x;
    header->source_pos_y = get_node_position(c->node)->y;
    
    TX(&c0, packet);
}


/* ************************************************** */
/* ************************************************** */
void rx(call_t *c, packet_t *packet) {  
  struct _cbr_private *nodedata = get_node_private_data(c);
  struct data_packet_header *header = (struct data_packet_header *) (packet->data + nodedata->overhead);

  printf("Node %d (%.2lf,%.2lf) received a packet from %d (%.2lf,%.2lf): seq=%d delay=%lfs size=%d bytes real_size=%d bits rxdBm=%lf dBm\n", c->node, get_node_position(c->node)->x, get_node_position(c->node)->y, header->source, header->source_pos_x, header->source_pos_y, header->sequence, ((get_time()*0.000000001)-header->delay), packet->size, packet->real_size, packet->rxdBm);

  packet_dealloc(packet);
}


/* ************************************************** */
/* ************************************************** */
application_methods_t methods = {rx};
