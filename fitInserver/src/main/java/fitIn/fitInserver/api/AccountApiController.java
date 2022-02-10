package fitIn.fitInserver.api;


import fitIn.fitInserver.domain.Account;
import fitIn.fitInserver.service.AccountService;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import java.util.List;
import java.util.stream.Collectors;


@RestController
@RequiredArgsConstructor
public class AccountApiController {


    private final AccountService accountService;


    //회원가입
    @PostMapping("/api/accounts")
    public CreateAccountResponse saveAccount(@RequestBody @Valid CreateAccountRequest request){

        Account account = new Account();

        account.setEmail(request.getEmail());
        account.setPassword(request.getPassword());
        account.setName(request.getName());
        Long id = accountService.join(account);
        return new CreateAccountResponse(id);
    }

    @Data
    static class CreateAccountResponse{
        private Long id;

        public CreateAccountResponse(Long id) {
            this.id = id;
        }
    }

    @Data
    static class CreateAccountRequest{

        @NotEmpty
        private String email;
        @NotEmpty
        private String password;
        @NotEmpty
        private String name;

    }

    //비밀번호 변경
    @PutMapping("/api/accounts/{id}")
    public UpdateAccountResponse updateAccount(@PathVariable("id") Long id,
                                               @RequestBody @Valid UpdateAccountRequest request){

        accountService.update(id, request.getPassword());
        Account findAccount = accountService.findOne(id);
        return new UpdateAccountResponse(findAccount.getId(),findAccount.getPassword());
    }

    @Data
    @AllArgsConstructor
    static class UpdateAccountResponse{
        private Long id;
        private String password;
    }

    @Data
    static class UpdateAccountRequest{
        private String password;
    }


    //회원 전체 이메일, 이름 조회
    @GetMapping("/api/accounts")
    public Accounts accounts(){
        List<Account> findAccounts = accountService.findAccounts();
        List<AccountDto> collect = findAccounts.stream()
                .map(m -> new AccountDto(m.getEmail(),m.getName()))
                .collect(Collectors.toList());
        return new Accounts(collect.size(), collect);
    }

    @Data
    @AllArgsConstructor
    static class Accounts<T>{
        private int count;
        private T data;

    }

    @Data
    @AllArgsConstructor
    static class AccountDto{
        private String email;
        private String name;
    }


}
