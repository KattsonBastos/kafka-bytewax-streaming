<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Kafka Event Processing with Bytewax</h3>

  <p align="center">
    Processing rides events from Kafka with Bytewax
  </p>
</div>

<br>
<p align="justify">
&ensp;&ensp;&ensp;&ensp;This repo contains a basic event processing example. The idea was to play around with Bytewax for event processing from Kafka. Bytewax is a lightweight, easy to install, and easy to deploy tool for real-time pipelines.
</p>

<br>

<!-- TABLE OF CONTENTS -->
## Contents

<details>
  <summary>Expand</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#development-plan">Development Plan</a></li>
        <li><a href="#business-context">Business Context</a></li>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#solution-description">Solution Description</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#quick-tip">Quick Tip</a></li>
        <li><a href="#prerequisites-and-installations">Prerequisites and Installations</a></li>
        <li><a href="#reproducing">Reproducing</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<br>

<!-- ABOUT THE PROJECT -->
## About The Project

<p align="center">
  <img src="./images/resources-diagram.png" >
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Making real-time data pipelines is really very challenging, since we have to deal with data volume changing, latency, data quality, many data sources, and so on. Another challenge we usually face is related to the processing tools: some of them can't process event-by-event, some of them are too expensive in a real fast scenario, and the deployment of some of them are really challenging. So, in order to better make decisions about our data stack, we have to properly understand the main options availables for storing and processing events.

&ensp;&ensp;&ensp;&ensp;In this way, the purpose of this repo is to get in touch with some stream processing capabilities of Bytewax. To achieve this goal, we ran a Kafka cluster in Docker and then produced fake ride (something like Uber's ride) data to a topic. Then, a Bytewax dataflow consumed those records, performed some transformations, adn then saved the refined data into another topic.
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Business Context

<p align="justify">
&ensp;&ensp;&ensp;&ensp;In order to be more business-like, we created a fake business context.

&ensp;&ensp;&ensp;&ensp;Our company <strong>KAB Rideshare</strong> is a company that provides ride-hailing services. Due to a recent increase in the number of users, KAB Rideshare will have to improve their data architecture and start processing the rides events for analytical purposes. So, our Data Team was given the task of implementing an event processing step. The company already stores all the events in a Kafka cluster, so our task is just to choose and implement the processing tool.
<br>
&ensp;&ensp;&ensp;&ensp;After some time of brainstorming, we decided to start with a MVP using a lightweight, but very powerful tool: Bytewax. In this, way, we can get the results wuickly so the analytical team can do their job. Once we have gained this time, we can better evaluate other solutions.
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Development Plan

<p align="justify">

- Implement the Data Gen
- Deploy a Kafka cluster on Docker for testing purposes
- Implement the Bytewax Dataflow

</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<p align="center">
  <img src="./images/resources-used.png" >
</p>


- <a href="https://www.python.org/" target="_blank">Python 3.8.16</a>
- <a href="https://beam.apache.org/" target="_blank">Kafka</a>
- <a href="https://www.terraform.io/" target="_blank">Bytewax</a>



<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Solution Description

<p align="justify">
&ensp;&ensp;&ensp;&ensp;We'll shortelly describe the workflow so you can better understand it.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;First of all, we need some data.
</p>


<p align="center">
  <img src="./images/workflow.png" >
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Actually, steps 2 and 3 could be just only one (we can decode the json and then return in as a dict), but, in order to explore some Beam's capabilities, we decided to separate them and use a function in the third step to convert the tuple return from the task 2 into a dict.
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;So, we'll end up with a table like this one:
</p>

<p align="center">
  <img src="./images/final-table.png" >
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Just a quick note: we used cloud storage to store Dataflow's job templates and temporary building files
</p>

<p align="justify">
&ensp;&ensp;&ensp;&ensp;For provisioning all cloud resources, we used Terraform. Actually, we used mainly because we had to continuously start and stop working in this solution, so, Terraform facilitates the creationg and destruction of resources.
</p>


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

<p align="justify">
&ensp;&ensp;&ensp;&ensp;You'll find in this section all the steps needed to reproduce this solution.
</p>

### Quick tip

<p align="justify">
&ensp;&ensp;&ensp;&ensp;I'm using <a href="https://www.gitpod.io/" target="_blank">Gitpod</a> to work on this project. Gitpod provides an initialized workspace integrated with some code repository, such as Github. In short, it is basically a VScode we access through the browser and it already has Python, Docker, and some other stuff installed, so we don't need to install things in our machine. They offer a free plan with up to 50 hour/mo (no credit card required), which is more than enough for practical projects (at least for me).
</p>

<p align="center">
  <img src="./images/gitpod.png" >
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites and Installations

* <a href="https://docs.docker.com/engine/install/" target="_blank"> Docker</a> and <a href="https://docs.docker.com/compose/install/" target="_blank"> Docker Compose</a>

* <a href="https://docs.bytewax.io/stable/guide/getting-started/installing.html" target="_blank"> Bytewax</a>

For other Python's dependencies, please refer to the `requirements.txt`, there we have all dependencies we need.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Reproducing

<p align="justify">
&ensp;&ensp;&ensp;&ensp;Before we begin, remember to take a look at following three files because they contain some variables related to GCP project ID, bucket names, and so on, that you'll need to change:
</p>

- `src/constants.py`
- `/src/infra/terraform.tfvars`
- `/src/infra/providers.tf`

1. Export env variables. In your machine, run in Terminal:
    ```sh
    export GOOGLE_PROJECT=<your_project_id>
    export GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_key_json_file>
    ```

2. Clone the repo:
    ```sh
    git clone https://github.com/KattsonBastos/dataflow-basic-streaming.git
    ```

3. Create a Python's virtual environment (I'm using virtualenv for simplicity) and activate it:
    ```sh
    python3 -m virtualenv env
    source env/bin/activate
    ```

4. Install Python's packages. Access the `src` folder and run the following command:
    ```sh
    pip install -r requirements.txt
    ```

5. Create terraform backend bucket
    ```sh
    gcloud storage buckets create gs:<bucket_name> --project=<project_id> --default-storage-class=STANDARD --location=us-east1
    ```
    Remember to change the bucket name in the <a href="https://github.com/KattsonBastos/dataflow-learning/blob/main/src/infra/providers.tf" target="_blank">Terraform provers file</a> and set yours.
    You can create it through the Console, if you want.

6. Create cloud resources with Terraform: <br>
    a) First, we need to initialize terraform. Go to the `src/infra/` folder and run:
    ```sh
    terraform init
    ```
    b) Then, the following command allows us to take a look at what resources are going to be created:
    ```sh
    terraform plan
    ```
    The resources file is the `main.tf`. There, we specify we want to create a Storage Bucket, a Bigquery Dataset, and Pub/Sub Topic and Subscription. The  `force_destroy = true` in the bucket creation allows us to destroy the bucket even if it is not empty (which acceptable since this is a practical project)

    c) Actually create the resources:
    ```sh
    terraform apply
    ```
    It will ask you to confirm the resource create.

7. Create the Dataflow Job Template. Run to the `src/` folder and run the following command (`constants.py` need to be updated with your config)
    ```sh
    python3 user_streaming.py
    ```
    Once it is done, you can the template saved in the `gs://<your_bucket/template/>

8. Then, we just have to run the Dataflow using this template. You can do it in the Console, or just run the following command:
   ```sh
   gcloud dataflow jobs run <a_name_you_want> --gcs-location gs://<your_bucket_name>/template/streaming_user_bq \
   --region us-east1 --staging-location gs://<your_bucket_name>/temp/
    ```
    After some time, you'll be able to see a new table in the BQ dataset, `users`, being populated.

9. Once you finished, remember to stop the streaming pipeline, otherwise it will drain your wallet and, then, destroy all resources if you don't need them anymore:
   ```sh
   gcloud dataflow jobs cancel <job_id> --force

   terraform destroy
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- NEXT STEPS -->
## Next Steps

From now on, we'll deploy both Kafka, bytewax, and the data generator to a Kubernetes cluster so we can better explore real world scenarios and the Bytewax scaling capabilities.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* <a href="https://www.youtube.com/watch?v=567kiizOY1U&t=3452s" target="_blank">Use-Case: Analisando Corridas do Uber em Tempo-Real com Kafka, Faust, Pinot e SuperSet | Live #80</a>: all the data transformations and the general idea of this repo was based on the referred live stream. The main difference is that here we changed the processing tool from Faust to Bytewax.
* <a href="https://github.com/bytewax/bytewax/tree/main/examples" target="_blank">Official bytewax examples</a>: they present amazing examples so we can easily get in touch with the tool.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


