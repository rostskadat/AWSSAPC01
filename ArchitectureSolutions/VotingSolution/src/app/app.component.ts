import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { APIService } from './API.service';
import { Vote } from '../types/vote';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'VotingSolution';
  public createForm: FormGroup;

  public votes: Array<Vote> = [];

  constructor(private api: APIService, private fb: FormBuilder) {
    this.createForm = this.fb.group({
      'election': ['', Validators.required],
      'vote': ['', Validators.required]
    });
  }

  async ngOnInit() {
    this.api.ListVotes().then(event => {
      this.votes = event.items as Array<Vote>;
    });
    this.api.OnCreateVoteListener.subscribe((event: any) => {
      const newVote = event.value.data.onCreateVote;
      this.votes = [newVote, ...this.votes];
    });
  }

  public onCreate(vote: Vote) {
    this.api.CreateVote(vote).then(event => {
      console.log('item created!');
      this.createForm.reset();
    })
      .catch(e => {
        console.log('error creating restaurant...', e);
      });
  }
}
