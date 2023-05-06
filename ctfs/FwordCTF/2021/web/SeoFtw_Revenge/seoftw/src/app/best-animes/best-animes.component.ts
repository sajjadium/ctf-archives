import { Component, OnInit } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-best-animes',
  templateUrl: './best-animes.component.html',
  styleUrls: ['./best-animes.component.css']
})
export class BestAnimesComponent implements OnInit {
  animes=[];
  li: any;
  constructor(private http : HttpClient) { }

  ngOnInit(): void {
    let parser = document.createElement('a');
    parser.href = window.location.href;
    let url="http://"+parser.hostname+":5000/"
    this.http.get(url).subscribe(Resp=>{
      console.log(Resp);
      this.li=Resp ;
      this.animes=this.li.animes;
    })

  }

}
